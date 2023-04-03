from django.db import models


class BookModel(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    language = models.CharField(max_length=100, blank=False, null=False)
    pages = models.PositiveIntegerField(blank=False, null=False)
    genre = models.CharField(max_length=50, blank=False, null=False)
    author = models.CharField(max_length=100, blank=False, null=False)
    release_year = models.PositiveIntegerField(blank=False, null=False)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False, null=False)
    description = models.TextField( max_length=5000 ,blank=True, null=False)
    image = models.ImageField(upload_to='shelf/files/book-covers/', default='shelf/files/default/default_cover.jpeg')

        
