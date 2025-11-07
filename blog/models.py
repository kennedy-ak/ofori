from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
import re
from html import unescape


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('technology', 'Technology'),
        ('politics', 'Politics'),
        ('life', 'Life'),
        ('advice', 'Advice'),
        ('others', 'Others'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=250, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='others')
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
        ]
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1
        while Post.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def get_reading_time(self):
        """Calculate reading time based on 200 words per minute"""
        # Strip HTML tags from content
        text = re.sub(r'<[^>]+>', '', self.content)
        word_count = len(text.split())
        reading_time = max(1, round(word_count / 200))
        return reading_time

    def get_excerpt(self):
        """Generate excerpt from content (150 characters, HTML-stripped)"""
        # Strip HTML tags
        text = re.sub(r'<[^>]+>', '', self.content)
        # Unescape HTML entities
        text = unescape(text)
        # Return first 150 characters
        if len(text) > 150:
            return text[:150] + '...'
        return text

    def get_like_count(self):
        """Get total number of likes for this post"""
        return self.likes.count()

    def is_liked_by(self, user):
        """Check if post is liked by specific user"""
        if user.is_authenticated:
            return self.likes.filter(user=user).exists()
        return False


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"
