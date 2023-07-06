from .models import Messages,RecentMsg
from rest_framework import serializers


def generate_room_name(sender,reciever):
    sorted_data = sorted([sender,reciever])
    result = f"{sorted_data[0]}_{sorted_data[1]}"
    return result

def format_roomname(name:str):
    if ' ' in name:
        name = name.replace(' ','_')
    return name

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


# todo serialize recent messages and return a list of dicts
class RecentMessageSerializer(serializers.ModelSerializer):
    time = serializers.CharField(source='last_msg.time')
    username = serializers.SerializerMethodField(read_only = True)
    profile_image = serializers.SerializerMethodField(read_only = True)
    last_msg = serializers.SerializerMethodField(read_only = True)
    id = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = RecentMsg
        fields=[
            'last_msg',
            'profile_image',
            'username',
            'time',
            'id'
        ]
    
    
    
    def get_contact(self,obj):
        current_user = self.context.get('user')
        user = obj.users.exclude(id= current_user.id)[0]
        return user
    
    
    
    def get_username(self,obj):
        user = self.get_contact(obj)
        return user.username
    
    def get_last_msg(self,obj):
        msg = obj.last_msg.message
        if len(msg) >= 18:
            return f"{msg[0:18]}..."
        else:
            return msg
    
    def get_profile_image(self,obj):
        user = self.get_contact(obj)
        return user.get_image_url()
    
    def get_id(self,obj):
        id = self.get_contact(obj).id
        return id
        