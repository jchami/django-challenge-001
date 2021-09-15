from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=256)
    picture = models.CharField(max_length=256)


class Article(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    summary = models.CharField(max_length=512)
    firstParagraph = models.CharField(max_length=1024)
    body = models.TextField()
