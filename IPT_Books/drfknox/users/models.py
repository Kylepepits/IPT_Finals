from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='book_images', null=True, blank=True)

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rental_date = models.DateTimeField(auto_now_add=True)
    return_due_date = models.DateTimeField(default=datetime.now()+timedelta(days=7))
    return_date = models.DateTimeField(null=True, blank=True)
    returned = models.BooleanField(default=False)
