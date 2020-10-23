from rest_framework import serializers
from .models import Message


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