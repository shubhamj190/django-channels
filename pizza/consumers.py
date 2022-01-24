from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync

from pizza.models import Order
class MyConsumer(WebsocketConsumer):

    def connect(self):
        self.channel_name="test_channel_name"
        self.room_group_name="test_group_name"
        async_to_sync(self.channel_layer.group_add)(self.channel_name, self.room_group_name)
        self.accept()
        self.send(text_data=json.dumps({'status':"websocket connected"}))
       
    def receive(self, text_data=None, bytes_data=None):
        print(text_data)

    def disconnect(self, close_code):
        print("diconnected")


class OrderProgess(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = 'order_%s' % self.room_name        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        order=Order.get_order_details(order_id=self.room_name)
        print(order)

        self.send(text_data=json.dumps(order))

    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'order_status',
                'payload': text_data
            }
        )


    def order_status(self, event):
        print(event)
        order = json.loads(event['value'])
        print("THISNIS NFJKDNFJKNDJKFNJDSNF",order)
        # Send message to WebSocket
        self.send(text_data=json.dumps(order))