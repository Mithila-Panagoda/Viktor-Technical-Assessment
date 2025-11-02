from django.db import models

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13,unique=True)
    cover_photo = models.FileField(upload_to='books/covers/',null=True,blank=True)
    def __str__(self):
        return self.name