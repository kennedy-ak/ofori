from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from .models import Post, Like
from .forms import PostForm
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
        'is_liked': post.is_liked_by(request.user),
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
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # Send newsletter notification if published
            if post.status == 'published':
                try:
                    send_new_post_notification(post)
                except Exception as e:
                    print(f"Error sending newsletter: {e}")

            messages.success(request, f'Post "{post.title}" created successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_edit_view(request, slug):
    """Edit an existing post (author or admin only)"""
    post = get_object_or_404(Post, slug=slug)

    # Check permissions
    if request.user != post.author and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('post_detail', slug=slug)

    # Track if post is being published for the first time
    was_draft = post.status == 'draft'

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            # Check if title changed and regenerate slug
            if post.title != form.cleaned_data['title']:
                post.slug = ''

            post = form.save()

            # Send newsletter notification if just published
            if was_draft and post.status == 'published':
                try:
                    send_new_post_notification(post)
                except Exception as e:
                    print(f"Error sending newsletter: {e}")

            messages.success(request, f'Post "{post.title}" updated successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
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
