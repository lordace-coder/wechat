import json
from channels.generic.websocket import WebsocketConsumer
from .models import Messages,CustomUser

from asgiref.sync import async_to_sync
class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        
        # create new msg obj
        data = dict()
        data['message'] = message
        data['username'] = username
        data['room_name'] = self.scope['url_route']['kwargs']['room_name']
        self.new_message(data)

        async_to_sync( self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'username': username,
            }
        )

    def chatroom_message(self, event):
        message = event['message']
        username = event['username']
        async_to_sync( self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        })))

    def new_message(self,data):
        sender = CustomUser.objects.get(username = data['username'])
        msg = Messages.objects.create(author = sender,reciever=data["room_name"],message=data["message"])
        print('saved')
        msg.save()
