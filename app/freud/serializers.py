from rest_framework import serializers
from .models import Chat, Message, MoodTracker, Journal
from authentication.serializers import ProfileSerializer


class ChatSerializer(serializers.ModelSerializer):
    
    user = ProfileSerializer(read_only=True)
    
    class Meta:
        model = Chat
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    
    chat = ChatSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = "__all__"
        

class MoodTrackerSerializer(serializers.ModelSerializer):
    
    user = ProfileSerializer(read_only=True)
    
    class Meta:
        model = MoodTracker
        fields = "__all__"
        

class JournalSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    
    class Meta:
        model = Journal
        fields = "__all__"