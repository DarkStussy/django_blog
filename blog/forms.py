from django import forms

from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class PostLikeForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('users_like',)
