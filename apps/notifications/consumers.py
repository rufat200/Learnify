import json
from channels.generic.websocket import AsyncWebsocketConsumer



class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("notifications", self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({
            "message": "Connected!"
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications", self.channel_name)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'event_type': event.get('event_type', 'unknown'),
        }))
