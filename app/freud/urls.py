from django.urls import path
from .views import (
    UserChatsListView, ChatMessagesListView, 
    ChatCreateView, ChatDeleteView, MessageCreateView,
    MoodTrackerCreateView, MoodTrackerListView
)

urlpatterns = [
    path('chats/', UserChatsListView.as_view(), name='user-chats'),
    path('chats/<int:chat_id>/messages/', ChatMessagesListView.as_view(), name='chat-messages'),
    path('chats/create/', ChatCreateView.as_view(), name='chat-create'),
    path('chats/<int:pk>/delete/', ChatDeleteView.as_view(), name='chat-delete'),
    path('chats/<int:chat_id>/messages/create/', MessageCreateView.as_view(), name='message-create'),
    path('mood-tracker/', MoodTrackerListView.as_view(), name='user-moods'),
    path('mood-tracker/create/', MoodTrackerCreateView.as_view(), name='moods-create'),   
]