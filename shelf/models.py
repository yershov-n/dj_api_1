from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=100, null=True, blank=True)


class Book(models.Model):
    name = models.CharField(max_length=150)
    annotation = models.CharField(max_length=1500)
    circulation = models.PositiveSmallIntegerField(null=True, blank=True)
    published = models.PositiveSmallIntegerField(null=True, blank=True)
