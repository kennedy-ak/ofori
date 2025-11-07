from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Newsletter
from .utils import send_welcome_email, send_reactivation_email


def newsletter_subscribe_view(request):
    """Subscribe to newsletter"""
    if request.method == 'POST':
        email = request.POST.get('email')

        if not email:
            messages.error(request, 'Email address is required.')
            return redirect(request.META.get('HTTP_REFERER', 'home'))

        # Check if email already exists
        existing_subscription = Newsletter.objects.filter(email=email).first()

        if existing_subscription:
            if existing_subscription.is_active:
                messages.info(request, 'You are already subscribed to our newsletter.')
            else:
                # Reactivate subscription
                existing_subscription.is_active = True
                existing_subscription.subscribed_at = timezone.now()
                existing_subscription.unsubscribed_at = None
                existing_subscription.save()

                # Send reactivation email
                try:
                    send_reactivation_email(email)
                except Exception as e:
                    print(f"Error sending reactivation email: {e}")

                messages.success(request, 'Welcome back! You have been resubscribed to our newsletter.')
        else:
            # Create new subscription
            Newsletter.objects.create(email=email)

            # Send welcome email
            try:
                send_welcome_email(email)
            except Exception as e:
                print(f"Error sending welcome email: {e}")

            messages.success(request, 'Successfully subscribed to our newsletter!')

        return redirect(request.META.get('HTTP_REFERER', 'home'))

    return redirect('home')


def newsletter_unsubscribe_view(request, email):
    """Unsubscribe from newsletter"""
    subscription = get_object_or_404(Newsletter, email=email)

    if request.method == 'POST':
        subscription.is_active = False
        subscription.unsubscribed_at = timezone.now()
        subscription.save()

        messages.success(request, 'You have been successfully unsubscribed from our newsletter.')
        return redirect('home')

    context = {
        'subscription': subscription,
    }

    return render(request, 'newsletter/unsubscribe.html', context)
