from .models import Movie, Preference, Comment
from .forms import CommentForm, UpdateMovieForm, CreateMovieForm
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from bootstrap_modal_forms.generic import BSModalCreateView
from urllib.parse import urlparse


def movie_list(request):
    # Main movie listing page
    movies = Movie.objects.all()
    return render(
        request, "movie_list.html", context={"movies": movies, "request": request}
    )


@login_required  # Decorator ensures only logged in users can access the page
def movie_detail(request, pk):
    # Detail movie view
    movie = Movie.objects.get(pk=pk)
    preference = Preference.objects.filter(movie__id=pk).values("user", "value")

    # Checking if the current user has liked/disliked the current movie
    pref_value = ""
    user_ids = {}
    for user in preference:
        user_ids[user["user"]] = user["value"]
    # user_ids = [id for id in user.values() for user in preference]
    # user_ids = [user.values() for user in preference]
    if request.user.id in user_ids.keys():
        if user_ids[request.user.id] == 1:
            pref_value = "LIKED"
        else:
            pref_value = "DISLIKED"

    # Create new comments - form data
    new_comment = None
    if request.method == "POST" and "comment" in request.POST:
        comment_form = CommentForm(
            data=request.POST, initial={"author": request.user.username}
        )
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.movie = movie
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    # Update movie form (only for superuser)
    if (
        request.method == "POST"
        and "update" in request.POST
        and request.user.is_superuser
    ):
        update_form = UpdateMovieForm(request.POST, instance=movie)
        if update_form.is_valid():
            update_form.save()
            update_form = UpdateMovieForm()

    else:
        update_form = UpdateMovieForm()

    # Parsing YouTube link to get ID to embed video
    youtube_link = movie.youtube_link
    p_link = urlparse(youtube_link)
    if p_link.netloc == "youtu.be":
        youtube_id = p_link.path[1:]
    elif p_link.netloc in ("www.youtube.com", "youtube.com"):
        if p_link.path == "/watch":
            id_index = p_link.query.index("v=")
            youtube_id = p_link.query[id_index + 2 : id_index + 13]
        elif p_link.path[:7] == "/embed/":
            youtube_id = p_link.path.split("/")[2]
        elif p_link.path[:3] == "/v/":
            youtube_id = p_link.path.split("/")[2]
    else:
        youtube_id = ""

    return render(
        request,
        "movie_detail.html",
        context={
            "movie": movie,
            "pref_value": pref_value,
            "youtube_id": youtube_id,
            "comment_form": comment_form,
            "update_form": update_form,
            "request": request,
        },
    )


@login_required
def preference(request, pk, userpreference):
    # Liking/Disliking functionality
    if request.method == "POST":
        movie = get_object_or_404(Movie, id=pk)
        obj = ""
        valueobj = ""
        try:
            obj = Preference.objects.get(user=request.user, movie=movie)
            valueobj = obj.value  # value of userpreference
            valueobj = int(valueobj)
            userpreference = int(userpreference)
            if valueobj != userpreference:
                obj.delete()
                upref = Preference()
                upref.user = request.user
                upref.movie = movie
                upref.value = userpreference
                if userpreference == 1 and valueobj != 1:
                    movie.likes += 1
                    movie.dislikes -= 1
                elif userpreference == 2 and valueobj != 2:
                    movie.dislikes += 1
                    movie.likes -= 1
                upref.save()
                movie.save()
                return redirect(movie_detail, pk)
            elif valueobj == userpreference:
                obj.delete()
                if userpreference == 1:
                    movie.likes -= 1
                elif userpreference == 2:
                    movie.dislikes -= 1
                movie.save()
                return redirect(movie_detail, pk)
        except Preference.DoesNotExist:
            upref = Preference()
            upref.user = request.user
            upref.movie = movie
            upref.value = userpreference
            userpreference = int(userpreference)
            if userpreference == 1:
                movie.likes += 1
            elif userpreference == 2:
                movie.dislikes += 1
            upref.save()
            movie.save()
            return redirect(movie_detail, pk)
    else:
        return redirect(movie_detail, pk)


def signup(request):
    # User signup form
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("movie_list")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})


class CreateMovieView(BSModalCreateView):
    # Create new movie Modal form
    template_name = "create_movie.html"
    form_class = CreateMovieForm
    success_message = "Success: Movie was created!"
    success_url = reverse_lazy("movie_list")


@method_decorator(
    user_passes_test(lambda u: u.is_superuser), name="dispatch"
)  # Decorator ensures only superuser can access the form
class DeleteMovieView(DeleteView):
    # Delete movie Class-Based View
    model = Movie
    success_url = reverse_lazy("movie_list")


def comment_delete(request, pk, commentid):
    # Delete comments
    if request.method == "POST":
        comment = get_object_or_404(Comment, id=commentid)
        comment.delete()
        return redirect(movie_detail, pk)
