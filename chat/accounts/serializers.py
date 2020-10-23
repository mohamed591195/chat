# we will make search for friends as it's
# but instead of send friend request
# we will make it send message-request --- not a friend-request
# a notification will be sent to the other user indicating that, there is a user want to message you
# if he accept a new thread will be made for them

# we will need a user detail page for each user

# if a user is a friend the button beside him should be send-message not friend;

from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):

    sender = serializers.CharField(source='sender.get_full_name', read_only=True)
    sender_url = serializers.CharField(source='sender.get_profile_url', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'sender', 'sender_url', 'content', 'seen', 'created_at']

