from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="events"
    )
    event_name = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to="event_images/")
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return self.event_name
