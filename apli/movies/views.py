from django.shortcuts import render, redirect
from .models import Movie
from .forms import CommentForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


def movie_list(request):    
    movies = Movie.objects.all()
    return render(request, 'movie_list.html', context={'movies': movies, 'request': request})


@login_required
def movie_detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    
    new_comment = None    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST, initial={'author': request.user.username})
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.movie = movie
            new_comment.user = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()
    
    return render(
        request,
        'movie_detail.html',
        context={
            'movie': movie,            
            'comment_form': comment_form,
            'request': request
        }
    )


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('movie_list')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})