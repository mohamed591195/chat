from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from .utils import handle_consumer_received_data


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        user = self.scope['user']

        if not user.is_authenticated:

            await self.close()

        else:

            self.devices_group_name = user.get_channels_group

            await self.channel_layer.group_add(
                self.devices_group_name,
                self.channel_name
            )
           
            await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.devices_group_name,
            self.channel_name
        )

        self.disconnect(close_code)

    async def receive(self, text_data):
        
        user = self.scope['user']

        data = json.loads(text_data)

        action = data.get('action')

        if action == 'update-user-status':

            data['channel_name'] = self.channel_name

        await sync_to_async(
            handle_consumer_received_data,
            thread_sensitive=True
        )(user, data)
   
    async def send_notification(self, event):

        notification = event['notification']

        await self.send(text_data=json.dumps({
            'notification': notification
        }))

    async def send_message(self, event):

        await self.send(text_data=json.dumps({
            'message': event['message']
        }))

    async def send_message_status(self, event):

        await self.send(text_data=json.dumps({
            'message_with_updated_status': event['message']
        }))
