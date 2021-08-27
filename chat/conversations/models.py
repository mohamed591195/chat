from django.db import models
from django.db.utils import cached_property
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Thread(TimeStamp):
    users = models.ManyToManyField(User, related_name='threads')
    # the title will only be used in threads that have more than two users
    title = models.CharField(max_length=50, blank=True, default='')
    
    def get_title(self, current_user):
        if not self.title:
            return self.users.exclude(id=current_user.id).first().get_full_name
        return self.title
        
    @cached_property
    def is_multi(self):
        if self.title:
            return True
        return False

    @cached_property
    def users_have_unseen_msgs(self):
        users = []
        for user in self.users.all():
            if self.messages.exclude(Q(sender=user) | Q(viewers=user)).count():
                users.append(user.id)
        return users

class Message(TimeStamp):

    MESSAGE_STATUS = (
        ('SEN', 'Seen'),
        ('DLV', 'Delivered'),
        ('SNT', 'Sent')
    )
    thread = models.ForeignKey(
        Thread, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(
        User, related_name='sent_messages', on_delete=models.SET_NULL, null=True)
    text = models.TextField()

    # if the message actually will be saved, it means that's sent from the client
    # so we make sent status as default
    status = models.CharField(choices=MESSAGE_STATUS, max_length=3, default='SNT')

    viewers = models.ManyToManyField(User)

    def __str__(self):
        return f'message from {self.sender} in thread {self.thread}'

class MessageRequest(models.Model):

    STATUS_CHOICES = (
        ('PEN', 'Pending'),
        ('ACT', 'Active')
    )
    user_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_message_requests')
    user_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_message_requests')
    status = models.CharField(
        default='PEN', choices=STATUS_CHOICES, max_length=3)
