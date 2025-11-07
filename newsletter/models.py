from django.db import models


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Newsletter Subscription'
        verbose_name_plural = 'Newsletter Subscriptions'
        ordering = ['-subscribed_at']

    def __str__(self):
        return f"{self.email} - {'Active' if self.is_active else 'Inactive'}"
