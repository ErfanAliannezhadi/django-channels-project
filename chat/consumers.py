import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import MessageModel, UserModel, ChatModel


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

        self.fetch_messages()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user_id = text_data_json["user_id"]

        self.save_new_message(message, user_id)
        auther = UserModel.objects.get(id=int(user_id)).username

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message, "auther": auther}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        auther = event["auther"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message, "auther": auther}))

    def save_new_message(self, content, user_id):
        chat = ChatModel.objects.filter(room_name=self.room_name).first()
        message = MessageModel(content=content, auther_id=user_id, chat=chat)
        message.save()

    def fetch_messages(self):
        messages = MessageModel.objects.filter(chat__room_name=self.room_name)
        for msg in messages:
            self.send(text_data=json.dumps({"message": msg.content, "auther": msg.auther.username}))
