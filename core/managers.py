from django.db import models


class PersonManager(models.Manager):
    def all_with_prefetch_movies(self):
        qs = self.get_queryset()
        return qs.prefetch_related("directed", "writing_credits", "role_set__movie")


class MovieManager(models.Manager):
    def all_with_related_persons(self):
        qs = self.get_queryset()
        qs = qs.select_related("director")
        qs = qs.prefetch_related("writers", "actors")
        return qs
