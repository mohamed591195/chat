from rest_framework import serializers
from .models import Message, Thread
from django.contrib.auth import get_user_model

User = get_user_model()


class ThreadUserSerilizer(serializers.ModelSerializer):

    image = serializers.CharField(source='image.url', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'get_full_name', 'image']
        
class ThreadSerializer(serializers.ModelSerializer):

    users = ThreadUserSerilizer(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = ['id', 'users', 'is_multi', 'users_have_unseen_msgs', 'title']

class ViewerImageField(serializers.RelatedField):
    def to_representation(self, value):
        return value.image.url

class MessageSerializer(serializers.ModelSerializer):

    sender_image = serializers.CharField(source='sender.image.url', read_only=True)
    viewers = ViewerImageField(many=True, read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'thread',
            'sender',
            'viewers',
            'sender_image',
            'text',
            'status',
            'created_at'
        ]