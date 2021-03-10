from django.conf import settings
from django.db import models
from django.utils import timezone

class Sheet(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    key = models.CharField(max_length=5)
    chords = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Playlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    playlist_name = models.CharField(max_length=200)
    sheets = models.ManyToManyField(Sheet, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.playlist_name
