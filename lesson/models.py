from django.db import models


class Daybook(models.Model):
    name = models.CharField(max_length=15)
    date = models.DateTimeField(auto_now_add=True)
    point = models.IntegerField(default=5)

    def __str__(self):
        return f'{self.name}:{self.point} - {self.date}'


class Person(models.Model):
    name = models.CharField(max_length=130)
    email = models.EmailField(blank=True)
    job_title = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
