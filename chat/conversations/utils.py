from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from accounts.serializers import NotificationSerializer
from .models import Thread, Message
from .serializers import MessageSerializer
from django.db.models import Q
from django.conf import settings
import redis

redis_cli = redis.StrictRedis(host=settings.REDIS_HOST, port=REDIS_PORT, db=settings.REDIS_DB)

channel_layer = get_channel_layer()

def send_updated_message_status(user, serialized_message):
    async_to_sync(channel_layer.group_send)(
            user.get_channels_group,
            {
                'type': 'send_message_status',
                'message': serialized_message.data
            }
        )

def handle_consumer_received_data(user, data):

    action = data.get('action')

    if action == 'send-message':

        thread = Thread.objects.get(id=data.get('threadId'))

        message = Message.objects.create(sender=user, thread=thread, text=data.get('text'))

        serialized_message = MessageSerializer(message)

        # being here means messages reached our server so
        # first we respond to sender, so message appears as sent
        send_updated_message_status(user, serialized_message)

        # then we try to send the message to every possible recipient in the thread
        for recipient in thread.users.exclude(id=user.id):

            async_to_sync(channel_layer.group_send)(
                recipient.get_channels_group,
                {
                    'type': 'send_message',
                    'message': serialized_message.data
                }
            )
    
    elif action == 'update-message-status':

        message = Message.objects.filter(id=data.get('messageId')).first()
        # status may be delivered or seen depending on the broweser tab status and other things
        message.status = data.get('status')

        # we add this user to be one of the message viewers
        message.viewers.add(user)
        message.save()

        serialized_message = MessageSerializer(message)
        # we send the new status to message sender
        send_updated_message_status(message.sender, serialized_message)

    elif action == 'set-latest-messages-seen':
        thread = user.threads.filter(id=data.get('threadId')).first()

        if thread:
            messages = thread.messages.exclude(Q(sender=user) | Q(status='SEN'))

            if messages.exists():
                
                for message in messages:
                    message.status = 'SEN'
                    message.viewers.add(user)
                    message.save()

                # we send the status of the last message so all of the above messages 
                # appears as sent 
                last_message = thread.messages.last()
                serialized_message = MessageSerializer(last_message)
                # we send the new status to message sender
                send_updated_message_status(last_message.sender, serialized_message)

    elif action == 'update-user-status':

        status = data.get('userStatus')
        channel_name = data.get('channel_name')

        away_set_key = f'user:{user.id}:away-channels'
        online_set_key = f'user:{user.id}:online-channels'
        user_status_key = f'user:{user.id}:status'

        if status == 'online':
            # remove from away set of channels if exist and add to online set
            redis_cli.srem(away_set_key, channel_name)
            redis_cli.sadd(online_set_key, channel_name)
            
        elif status == 'away':
            redis_cli.srem(online_set_key, channel_name)
            redis_cli.sadd(away_set_key, channel_name)

        # offline case will be triggered from the consumer when disconnect from channel
        elif status == 'offline':
            # we make sure the channel not any set
            redis_cli.srem(away_set_key, channel_name)
            redis_cli.srem(online_set_key, channel_name)


        # finally we update the overall status of the user

        # 1) if the online set is not empty
        if redis_cli.scard(online_set_key):
            redis_cli.set(user_status_key, 'online')

        # 2) being here mean online set it empty, so we check away set
        elif redis_cli.scard(away_set_key):
            redis_cli.set(user_status_key, 'away')

        # 3) both sets are empty means user is offline
        else:
            redis_cli.set(user_status_key, 'offline')

        # sending status to online friends
        # bad implementation
        for thread in user.threads.all():

            friends = thread.users.exlude(id=user.id)

            for friend in friends:

                if redis_cli.get(f'user:{friend.id}:status') == 'online':

                    async_to_sync(channel_layer.group_send)(
                        friend.get_channels_group,
                        {
                            'type': 'send_message',
                            'message': 'serialized_message.data'
                        }
                    )
    
               
def send_notification(notification):

    if notification.verb == 'message request':

        notification.content = 'sent you a message request'
        notification.save()


    elif notification.verb == "accepted message request":

        notification.content = 'accepted your message request'
        notification.save()

    serialized_notification = NotificationSerializer(notification)

    # there will be one recipient in friend requests
    target_user_group = notification.recipients.first().get_channels_group
 
    async_to_sync(channel_layer.group_send)(

        target_user_group,
        {
            'type': 'send_notification',
            'notification': serialized_notification.data
        }
    )



