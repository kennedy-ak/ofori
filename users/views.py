from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from .models import UserProfile


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        # Validation
        if not all([username, email, password, password_confirm]):
            messages.error(request, 'All fields are required.')
            return render(request, 'users/register.html')

        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'users/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'users/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'users/register.html')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        messages.success(request, 'Registration successful! Please wait for admin approval before you can create posts.')
        login(request, user)
        return redirect('home')

    return render(request, 'users/register.html')


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'users/login.html')


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def user_profile_view(request, username):
    """View user profile and their posts"""
    user = get_object_or_404(User, username=username)
    profile = user.profile

    # Get user's published posts
    posts = user.posts.filter(status='published').order_by('-created_at')

    context = {
        'profile_user': user,
        'profile': profile,
        'posts': posts,
    }

    return render(request, 'users/profile.html', context)


@login_required
def dashboard_view(request):
    """User dashboard showing all their posts"""
    posts = request.user.posts.all().order_by('-created_at')

    # Count stats
    total_posts = posts.count()
    published_posts = posts.filter(status='published').count()
    draft_posts = posts.filter(status='draft').count()

    context = {
        'posts': posts,
        'total_posts': total_posts,
        'published_posts': published_posts,
        'draft_posts': draft_posts,
    }

    return render(request, 'users/dashboard.html', context)


def is_admin(user):
    """Check if user is admin"""
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin)
def admin_dashboard_view(request):
    """Admin dashboard for managing user approvals"""
    pending_users = UserProfile.objects.filter(is_approved=False).select_related('user')

    context = {
        'pending_users': pending_users,
    }

    return render(request, 'users/admin_dashboard.html', context)


@user_passes_test(is_admin)
def approve_user_view(request, user_id):
    """Approve a user to allow them to create posts"""
    profile = get_object_or_404(UserProfile, id=user_id)

    if not profile.is_approved:
        profile.is_approved = True
        profile.approved_at = timezone.now()
        profile.save()
        messages.success(request, f'{profile.user.username} has been approved!')
    else:
        profile.is_approved = False
        profile.approved_at = None
        profile.save()
        messages.info(request, f'{profile.user.username} approval has been revoked.')

    return redirect('admin_dashboard')
