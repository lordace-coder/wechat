from .models import Messages
from rest_framework import serializers


def generate_room_name(sender,reciever):
    sorted_data = sorted([sender,reciever])
    result = f"{sorted_data[0]}_{sorted_data[1]}"
    return result


class MessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='author.username')
    class Meta:
        model = Messages
        fields = [
            'username',
            'message',
            'reciever',
            'time'
        ]