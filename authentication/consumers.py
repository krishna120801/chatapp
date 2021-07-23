from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth.models import User
class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name=''
        self.room_name1 =self.scope['url_route']['kwargs']['room_name']
        self.room_name+=''.join(sorted(self.room_name1))
        self.room_group = 'chat_87105116104%s' % self.room_name
        print(self.room_group)
        await self.channel_layer.group_add(
            self.room_group,
            self.channel_name
        )

        await self.accept()

        '''await self.channel_layer.group_send(
            self.room_group,{
                'type': 'test_mess',
                'tester':'hello_world',
            }
        )'''
    try:
        async def test_mess(self,event):
            print('receive',event)
            tester = event['message']
            sender = event['sender']

            await self.send(text_data = json.dumps({
                'tester':tester,
                'sender':sender
                }))
    except:
        pass

    async def disconn(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group,
            self.channel_name
        )
    async def receive (self , text_data):
        text_data_json= json.loads(text_data)
        message= text_data_json['message']
        sender= text_data_json['sender']

        await self.channel_layer.group_send(
                self.room_group,{
                'type':'chatroom',
                'message': message,
                'sender': sender,
                })
    async def chatroom(self,event):
        message= event['message']
        sender=event['sender']
        await self.send(text_data=json.dumps({
            'message':message,
            'sender':sender,
        }))