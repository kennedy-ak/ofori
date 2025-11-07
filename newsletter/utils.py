from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_welcome_email(email):
    """Send welcome email to new newsletter subscriber"""
    subject = 'Welcome to Ofori Blog Newsletter!'

    html_message = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #007bff;">Welcome to Ofori Blog!</h2>
                <p>Thank you for subscribing to our newsletter. You'll now receive updates whenever we publish new content.</p>
                <p>Stay tuned for:</p>
                <ul>
                    <li>Latest blog posts</li>
                    <li>Technology insights</li>
                    <li>Life advice and more</li>
                </ul>
                <p>We're excited to have you with us!</p>
                <hr style="border: 1px solid #eee; margin: 20px 0;">
                <p style="font-size: 12px; color: #666;">
                    Don't want these emails?
                    <a href="{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'}/newsletter/unsubscribe/{email}/">Unsubscribe</a>
                </p>
            </div>
        </body>
    </html>
    """

    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        html_message=html_message,
        fail_silently=False,
    )


def send_reactivation_email(email):
    """Send reactivation email to returning subscriber"""
    subject = 'Welcome Back to Ofori Blog!'

    html_message = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #007bff;">Welcome Back!</h2>
                <p>We're thrilled to have you back on our newsletter list.</p>
                <p>You'll now receive updates about our latest posts and content.</p>
                <p>Thank you for rejoining our community!</p>
                <hr style="border: 1px solid #eee; margin: 20px 0;">
                <p style="font-size: 12px; color: #666;">
                    Don't want these emails?
                    <a href="{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'}/newsletter/unsubscribe/{email}/">Unsubscribe</a>
                </p>
            </div>
        </body>
    </html>
    """

    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        html_message=html_message,
        fail_silently=False,
    )


def send_new_post_notification(post):
    """Send email notification to all active subscribers when a new post is published"""
    from .models import Newsletter

    active_subscribers = Newsletter.objects.filter(is_active=True)

    if not active_subscribers.exists():
        return

    subject = f'New Post: {post.title}'

    for subscriber in active_subscribers:
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #007bff;">New Post Published!</h2>
                    <h3>{post.title}</h3>
                    <p><strong>By:</strong> {post.author.get_full_name() or post.author.username}</p>
                    <p><strong>Category:</strong> {post.get_category_display()}</p>
                    <p>{post.get_excerpt()}</p>
                    <p>
                        <a href="http://{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'}{post.get_absolute_url()}"
                           style="display: inline-block; padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">
                            Read Full Post
                        </a>
                    </p>
                    <hr style="border: 1px solid #eee; margin: 20px 0;">
                    <p style="font-size: 12px; color: #666;">
                        You're receiving this because you subscribed to Ofori Blog newsletter.
                        <a href="http://{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'}/newsletter/unsubscribe/{subscriber.email}/">Unsubscribe</a>
                    </p>
                </div>
            </body>
        </html>
        """

        plain_message = strip_tags(html_message)

        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [subscriber.email],
            html_message=html_message,
            fail_silently=True,
        )
