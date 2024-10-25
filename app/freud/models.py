from django.db import models
from helpers.models import TrackingModel
from authentication.models import User


class Chat(TrackingModel):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

class Message(TrackingModel):
    content = models.TextField()
    is_user = models.BooleanField(default=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    

#mood possibility [depressed, sad, neutral, happy, overjoyed]
class MoodTracker(TrackingModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(max_length=10)
    

class Journal(TrackingModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    mood = models.CharField(max_length=10)
    stress_level = models.IntegerField()