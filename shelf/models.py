from django.db import models


class BookModel(models.Model):
    name = models.CharField(max_length=200, blank=False)
    language = models.CharField(max_length=100, blank=False)
    pages = models.IntegerField()
    genre = models.CharField(max_length=50, blank=False)
    author = models.CharField(max_length=100, blank=False)
    realease_year = models.IntegerField()