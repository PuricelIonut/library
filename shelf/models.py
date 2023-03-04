from django.db import models


class BookModel(models.Model):
    title = models.CharField(max_length=200, blank=False)
    language = models.CharField(max_length=100, blank=False)
    pages = models.IntegerField()
    genre = models.CharField(max_length=50, blank=False)
    author = models.CharField(max_length=100, blank=False)
    release_year = models.IntegerField()
    quantity = models.IntegerField(default=0)
    description = models.TextField( max_length=5000 ,blank=True, null=False)
    image = models.ImageField(upload_to='shelf/files/book-covers/', default='shelf/files/default/default_cover.jpeg')

    def add_stock(self, quantity_to_add: int):
        return self.quantity + quantity_to_add

    def remove_stock(self, quantity_to_remove: int):
        if quantity_to_remove > self.quantity:
            raise ValueError('Not enough stock!')
        else:
            return self.quantity - quantity_to_remove
        
