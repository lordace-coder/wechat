from .models import Messages,CustomUser
from rest_framework import serializers


def generate_room_name(sender,reciever):
    sorted_data = sorted([sender,reciever])
    result = f"{sorted_data[0]}_{sorted_data[1]}"
    return result


class MessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='author.username')
    profile_image = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Messages
        fields = [
            'username',
            'message',
            'reciever',
            'time',
            'profile_image'
        ]

    def get_profile_image(self,obj):
        return obj.author.get_image_url()

def format_roomname(name:str):
    if ' ' in name:
        name = name.replace(' ','_')
    return name


def user_to_dict(instance:CustomUser)->dict:
    user = dict()
    user['username'] = instance.username
    user['email'] = instance.email
    user['bio'] = instance.bio
    user['id'] = instance.id
    user['profile_image'] = instance.profile_image.url
    return user