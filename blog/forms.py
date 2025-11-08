from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Post


class PostForm(forms.ModelForm):
    """Form for creating and editing blog posts with Summernote editor"""

    class Meta:
        model = Post
        fields = ['title', 'category', 'created_at', 'content', 'image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'created_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'content': SummernoteWidget(attrs={
                'summernote': {
                    'width': '100%',
                    'height': '400px',
                }
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'title': 'Title *',
            'category': 'Category *',
            'created_at': 'Publication Date *',
            'content': 'Content *',
            'image': 'Featured Image',
            'status': 'Status *',
        }
        help_texts = {
            'created_at': 'Select the date and time for this post.',
            'content': 'Use the rich text editor to format your content.',
            'status': 'Draft posts are only visible to you. Published posts are visible to everyone and will trigger newsletter notifications.',
        }
