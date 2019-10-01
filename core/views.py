from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Movie, Person


class MovieList(ListView):
    model = Movie
    paginate_by = 5


class MovieDetail(DetailView):
    queryset = Movie.objects.all_with_related_persons()


class PersonDetail(DetailView):
    queryset = Person.objects.all_with_prefetch_movies()


def view_404(request, *args, **kwargs):
    return render(request, "404.html")

