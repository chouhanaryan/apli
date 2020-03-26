from django.shortcuts import render
from .models import Movie
from .forms import CommentForm

def movie_list(request):    
    movies = Movie.objects.all()
    return render(request, 'movie_list.html', context={'movies': movies})

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
            # 'new_comment': new_comment,
            'comment_form': comment_form,
            'request': request
        }
    )