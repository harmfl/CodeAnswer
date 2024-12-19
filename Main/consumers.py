from channels.generic.websocket import WebsocketConsumer
import json


class CSDNDataConsumer(WebsocketConsumer):
    def connect(self):
        # 假设我们使用用户的 ID 作为组名
        user_id = self.scope.get('user', None)
        if user_id is not None:
            self.group_name = f'user_{user_id}'
        else:
            self.group_name = f'anonymous_{self.channel_name}'  # 如果没有用户，则使用 channel_name 作为组名

        # 将消费者加入到该组
        self.channel_layer.group_add(self.group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        # 消费者断开连接时从组中移除
        self.channel_layer.group_discard(self.group_name, self.channel_name)

    def receive(self, text_data):
        # 处理来自客户端的消息
        data = json.loads(text_data)
        self.send(text_data=json.dumps({
            'message': f'Received: {data["message"]}'
        }))

    def chat_message(self, event):
        # 处理从其他地方发送到该组的消息
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))