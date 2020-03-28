from .models import Movie
from .forms import CommentForm, UpdateMovieForm, CreateMovieForm
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from bootstrap_modal_forms.generic import BSModalCreateView
from urllib.parse import urlparse


def movie_list(request):
    
    ''' Main movie listing page '''
    movies = Movie.objects.all()
    return render(request, 'movie_list.html', context={'movies': movies, 'request': request})


# Decorator ensures only logged in users can access the page
@login_required
def movie_detail(request, pk):
    
    movie = Movie.objects.get(pk=pk)

    ''' Create new comments - form data '''
    new_comment = None    
    if request.method == 'POST' and 'comment' in request.POST:
        comment_form = CommentForm(data=request.POST, initial={'author': request.user.username})
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.movie = movie
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    
    
    ''' Update movie form (only for superuser) '''
    if request.method == 'POST' and 'update' in request.POST and request.user.is_superuser:
        update_form = UpdateMovieForm(request.POST, instance=movie)
        if update_form.is_valid():
            update_form.save()
            update_form = UpdateMovieForm()

    else:
        update_form = UpdateMovieForm()


    ''' Parsing YouTube link to get ID to embed video '''
    youtube_link = movie.youtube_link
    p_link = urlparse(youtube_link)
    if p_link.netloc == 'youtu.be':
        youtube_id = p_link.path[1:]
    elif p_link.netloc in ('www.youtube.com', 'youtube.com'):
        if p_link.path == '/watch':
            id_index = p_link.query.index('v=')
            youtube_id = p_link.query[id_index+2:id_index+13]
        elif p_link.path[:7] == '/embed/':
            youtube_id = p_link.path.split('/')[2]
        elif p_link.path[:3] == '/v/':
            youtube_id = p_link.path.split('/')[2]
    else:
        youtube_id = ''


    return render(
        request,
        'movie_detail.html',
        context={
            'movie': movie,
            'youtube_id': youtube_id,
            'comment_form': comment_form,
            'update_form': update_form,
            'request': request
        }
    )


def signup(request):

    ''' User signup form '''
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


class CreateMovieView(BSModalCreateView):
    
    ''' Create new movie Modal form '''
    template_name = 'create_movie.html'
    form_class = CreateMovieForm
    success_message = 'Success: Movie was created!'
    success_url = reverse_lazy('movie_list')


# Decorator ensures only superuser can access the form
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class DeleteMovieView(DeleteView):

    ''' Delete movie Class-Based View '''
    model = Movie
    success_url = reverse_lazy('movie_list')