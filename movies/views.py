from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


@login_required
def home(request):

    query = request.GET.get('q')

    if query:
        movies = Movie.objects.filter(title__icontains=query)
    else:
        movies = Movie.objects.all()

    return render(request, 'home.html', {'movies': movies})


@login_required
def movie_detail(request, id):

    movie = get_object_or_404(Movie, id=id)

    recommended_movies = Movie.objects.filter(
        genre=movie.genre
    ).exclude(id=movie.id)

    return render(request, 'movie_detail.html', {
        'movie': movie,
        'recommended_movies': recommended_movies
    })


def signup(request):

    form = UserCreationForm()

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('/login/')

    return render(request, 'signup.html', {'form': form})
