from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Chat, Message, MoodTracker
from .serializers import ChatSerializer, MessageSerializer, MoodTrackerSerializer
from django.views.decorators.csrf import csrf_exempt    
from utils.gemini import GeminiApi

# Retrieve all chats for the logged-in user
class UserChatsListView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user)


# Retrieve all messages for a specific chat (owned by the logged-in user)
class ChatMessagesListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs.get('chat_id')
        return Message.objects.filter(chat__id=chat_id, chat__user=self.request.user)


# Create a new chat
class ChatCreateView(generics.CreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Delete a specific chat (owned by the logged-in user)
class ChatDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user)
    
    @csrf_exempt  # Disable CSRF for this view
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# Create a new message in a specific chat (owned by the logged-in user)
class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        chat_id = self.kwargs.get('chat_id')
        chat = Chat.objects.get(id=chat_id, user=self.request.user)
        serializer.save(chat=chat)
        
class MessageCreateView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        chat_id = self.kwargs.get('chat_id')
        chat = Chat.objects.get(id=chat_id, user=self.request.user)

        # Retrieve previous messages as history for the Gemini API
        history = [
            {"role": "user" if message.is_user else "model", "parts": message.content}
            for message in Message.objects.filter(chat=chat).order_by('created_at')
        ]

        # Initialize the chatbot with the existing history
        chatbot = GeminiApi()
        chatbot.start_chat(initial_history=history)

        # Add the new user message
        user_message = serializer.save(is_user=True, chat=chat)

        # Send the new message to the chatbot and get the response
        chatbot_response_text = chatbot.send_message(user_message.content)

        # Save the chatbot's response to the database
        Message.objects.create(
            content=chatbot_response_text,
            is_user=False,
            chat=chat
        )

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        chat_id = self.kwargs.get('chat_id')
        chat = Chat.objects.get(id=chat_id, user=self.request.user)
        messages = Message.objects.filter(chat=chat).order_by('created_at')
        return Response({
            'messages': MessageSerializer(messages, many=True).data
        })


# create new MoodTracker
class MoodTrackerCreateView(generics.CreateAPIView):
    serializer_class = MoodTrackerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

class MoodTrackerListView(generics.ListAPIView):
    serializer_class = MoodTrackerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MoodTracker.objects.filter(user=self.request.user)