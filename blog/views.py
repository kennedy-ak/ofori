from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from .models import Post, Like
from newsletter.utils import send_new_post_notification


def home_view(request):
    """Home page showing all published posts"""
    posts = Post.objects.filter(status='published').select_related('author').prefetch_related('likes')

    # Category filter
    category = request.GET.get('category')
    if category:
        posts = posts.filter(category=category)

    context = {
        'posts': posts,
        'selected_category': category,
    }

    return render(request, 'blog/home.html', context)


def post_detail_view(request, slug):
    """View individual post details"""
    post = get_object_or_404(
        Post.objects.select_related('author').prefetch_related('likes'),
        slug=slug
    )

    # Only show published posts unless user is the author or staff
    if post.status != 'published':
        if not request.user.is_authenticated or (request.user != post.author and not request.user.is_staff):
            messages.error(request, 'This post is not available.')
            return redirect('home')

    context = {
        'post': post,
    }

    return render(request, 'blog/post_detail.html', context)


@login_required
def post_create_view(request):
    """Create a new blog post (approved users only)"""
    # Check if user is approved
    if not request.user.profile.is_approved:
        messages.error(request, 'You must be approved by an admin before you can create posts.')
        return redirect('home')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        status = request.POST.get('status', 'draft')
        image = request.FILES.get('image')

        # Validation
        if not all([title, content, category]):
            messages.error(request, 'Title, content, and category are required.')
            return render(request, 'blog/post_form.html')

        # Create post
        post = Post.objects.create(
            title=title,
            content=content,
            category=category,
            status=status,
            author=request.user,
            image=image
        )

        # Send newsletter notification if published
        if status == 'published':
            try:
                send_new_post_notification(post)
            except Exception as e:
                print(f"Error sending newsletter: {e}")

        messages.success(request, f'Post "{title}" created successfully!')
        return redirect('post_detail', slug=post.slug)

    return render(request, 'blog/post_form.html')


@login_required
def post_edit_view(request, slug):
    """Edit an existing post (author or admin only)"""
    post = get_object_or_404(Post, slug=slug)

    # Check permissions
    if request.user != post.author and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('post_detail', slug=slug)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        status = request.POST.get('status', 'draft')
        image = request.FILES.get('image')

        # Validation
        if not all([title, content, category]):
            messages.error(request, 'Title, content, and category are required.')
            return render(request, 'blog/post_form.html', {'post': post})

        # Track if post is being published for the first time
        was_draft = post.status == 'draft'
        is_now_published = status == 'published'

        # Update post
        post.title = title
        post.content = content
        post.category = category
        post.status = status

        if image:
            post.image = image

        # Regenerate slug if title changed
        if post.title != title:
            post.slug = ''

        post.save()

        # Send newsletter notification if just published
        if was_draft and is_now_published:
            try:
                send_new_post_notification(post)
            except Exception as e:
                print(f"Error sending newsletter: {e}")

        messages.success(request, f'Post "{title}" updated successfully!')
        return redirect('post_detail', slug=post.slug)

    context = {
        'post': post,
        'is_edit': True,
    }

    return render(request, 'blog/post_form.html', context)


@login_required
def post_delete_view(request, slug):
    """Delete a post (author or admin only)"""
    post = get_object_or_404(Post, slug=slug)

    # Check permissions
    if request.user != post.author and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('post_detail', slug=slug)

    if request.method == 'POST':
        post_title = post.title
        post.delete()
        messages.success(request, f'Post "{post_title}" deleted successfully!')
        return redirect('dashboard')

    context = {
        'post': post,
    }

    return render(request, 'blog/post_confirm_delete.html', context)


@login_required
def post_like_view(request, slug):
    """Toggle like on a post"""
    post = get_object_or_404(Post, slug=slug)

    # Check if user already liked the post
    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        # Unlike if already liked
        like.delete()
        liked = False
    else:
        liked = True

    # Return JSON response for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'like_count': post.get_like_count(),
        })

    # Redirect back for regular requests
    return redirect('post_detail', slug=slug)


def search_view(request):
    """Search posts by title and content"""
    query = request.GET.get('q', '')
    posts = Post.objects.none()

    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            status='published'
        ).select_related('author').prefetch_related('likes')

    context = {
        'posts': posts,
        'query': query,
    }

    return render(request, 'blog/search.html', context)
