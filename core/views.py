from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import VoteForm
from .models import Movie, Person, Vote


class MovieList(ListView):
    model = Movie
    paginate_by = 5


class MovieDetail(DetailView):
    queryset = Movie.objects.all_with_related_persons()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(
                movie=self.object, user=self.request.user
            )
            if vote.id:
                vote_form_url = reverse(
                    "core:UpdateVote", kwargs={"movie_id": vote.movie.id, "pk": vote.id}
                )
            else:
                vote_form_url = reverse("core:CreateVote", kwargs={"movie_id": self.object.id})
            vote_form = VoteForm(instance=vote)
            ctx["vote_form"] = vote_form
            ctx["vote_form_url"] = vote_form_url
        return ctx


class PersonDetail(DetailView):
    queryset = Person.objects.all_with_prefetch_movies()


class CreateVote(LoginRequiredMixin, CreateView):
    form_class = VoteForm

    def get_initial(self):
        initial = super().get_initial()
        initial["user"] = self.request.id
        initial["movie"] = self.kwargs["movie_id"]
        return initial

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse("core:MovieDetail", kwargs={"pk": movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = context["object"].id
        movie_detail_url = reverse("core:MovieDetail", kwargs={"pk": movie_id})
        return redirect(movie_detail_url)


def view_404(request, *args, **kwargs):
    return render(request, "404.html")
