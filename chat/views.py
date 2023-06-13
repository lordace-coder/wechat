from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .helpers import MessageSerializer, generate_room_name,format_roomname
from .models import Messages,CustomUser,Groups

@login_required()
def index(request):
    current_user = request.user
    users = CustomUser.objects.exclude(id=current_user.id)
    groups = Groups.objects.all()
    return render(request, 'index.html', {"users":users,"groups":groups})



@login_required()
def room(request, userId):
    recipent = CustomUser.objects.get(id=userId).username
    username = request.user.username
    room_name = generate_room_name(recipent,username)
    return render(request, 'room.html', {
        'room_name': room_name,
        'username':username,
        'recipient':recipent,
        'private_room':'true'
    })


# for group rooms
@login_required()
def group_room(request, groupName):
    if not Groups.objects.filter(name=groupName).exists():
        raise Http404
    
    
    recipent = groupName
    username = request.user.username
    room_name = format_roomname(groupName)
    return render(request, 'room.html', {
        'room_name': room_name,
        'username':username,
        'recipient':recipent,
        'private_room':'false'
        
    })




# # grab messages on entering room
# # api response
@login_required()
@api_view(["GET"])
def get_messages(request,roomName):
    if Groups.objects.filter(name=roomName).exists():
        group = Groups.objects.get(name=roomName)
        messages = Messages.objects.filter(group = group)
        serialized_data = MessageSerializer(messages,many=True)
        return Response(serialized_data.data)
    if request.user.username not in roomName:
        return Response(status=404)
    messages = Messages.objects.filter(reciever = roomName)
    serialized_data = MessageSerializer(messages,many=True)
    return Response(serialized_data.data)

#todo Add chat a random person functionality

# ! Authentication views

def login(request):
    if request.method ==  'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.info(request,"invalid username or password")
    return render(request,'login.html',{})


@login_required()
def logout(request):
    auth.logout(request)
    return redirect("login")



def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            if len(password) >= 8 :
                if not CustomUser.objects.filter(username=username).exists():
                    user = CustomUser.objects.create(
                        username = username,
                        password=password,
                        email=email
                    )
                    
                    user.save()
                    auth.login(request,user)
                    return redirect("index")
                else:
                    messages.info(request,'username already exists')
                    return redirect('signup')
            else:
                messages.info(request,"password cant be less than 8 characters")
                return redirect('signup')
                
        else:
            messages.info(request,"passwords dont match")
            return redirect('signup')
    
    return render(request,'signup.html',{})


#todo: Add password recovery view here