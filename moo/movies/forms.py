from .models import Movie, Comment
from django import forms
from bootstrap_modal_forms.forms import BSModalForm


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': 'Comment'}


class UpdateMovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('title', 'youtube_link')
        labels = {'youtube_link': 'YouTube Link'}


class CreateMovieForm(BSModalForm):
    class Meta:
        model = Movie
        fields = ('title', 'youtube_link')
        labels = {'youtube_link': 'YouTube Link'}