from typing import Any
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views import generic
from .helpers import MessageSerializer, format_roomname, generate_room_name,user_to_dict
from .models import CustomUser, Groups, Messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q



class IndexView(LoginRequiredMixin,generic.TemplateView):
    template_name = 'index.html'
    
    def get_context(self)->dict:
        request = self.request
        current_user = self.request.user
        users = CustomUser.objects.none()
       
       
    #    * check for recent chats
        if 'recent_chats' in request.session:
           users:list = request.session['recent_chats']
        else:
            request.session['recent_chats'] = list()
            users:list = request.session['recent_chats']
            
        users.reverse() 
        context = {
            "users":users,
            'view_name':'index'
        }
        return context
    
    
    
    def get(self,*args, **kwargs):
        context = self.get_context()
        return render(self.request, 'index.html', context)
    
    
index = IndexView.as_view()






class GroupChatView(IndexView):
    
    def get_context(self)->dict:
        current_user = self.request.user
        groups = Groups.objects.all()
       
        context = {
            "groups":groups,
            'view_name':'index'
        }
        return context
        


class ListUsersView(IndexView):
    template_name = 'list_users.html'
    def get_object(self):
        obj = CustomUser.objects.exclude(id=self.request.user.id).order_by('?')
        return obj
    def get_context(self,obj = None)->dict:
        context = super().get_context()
        context['users'] = CustomUser.objects.exclude(id=self.request.user.id).order_by('?')
        if obj:
            context['users'] = obj
        return context 
    def get(self, *args, **kwargs):
        obj = None
        if 'q' in self.request.GET:
            q = self.request.GET['q']
            multiple_q = Q(Q(username__icontains=q)|Q(email__icontains=q))
            obj = self.get_object().filter(multiple_q).order_by('username')
        return render(self.request,self.template_name,self.get_context(obj))



@login_required()
def room(request, userId):
    recipent = CustomUser.objects.get(id=userId)
    # if recipent in sessions remove and add back to the top of the list
    reciever = user_to_dict(recipent)
    for i in request.session['recent_chats']:
        if i['id'] == reciever['id']:
            request.session['recent_chats'].remove(i)
    if reciever in request.session['recent_chats']:
        request.session['recent_chats'].remove(reciever)
        request.session['recent_chats'].append(reciever)
        request.session.modified = True
        
    else:
        request.session['recent_chats'].append(reciever)
        
        request.session.modified = True
    # else add recipent to sessions
    username = request.user.username
    room_name = generate_room_name(recipent.username,username)
    return render(request, 'room.html', {
        'room_name': room_name,
        'username':username,
        'recipient':recipent.username,
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
        bio = request.POST['bio']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if ' ' in username:
            messages.info(request,"Username cant contain a 'space' ")
            return redirect('signup')
        if password == confirm_password:
            if len(password) >= 8 :
                if not CustomUser.objects.filter(username=username).exists():
                    user = CustomUser.objects.create(
                        username = username,
                        password=password,
                        email=email,
                        bio=bio
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


# *profile view
class ProfileDetailView(generic.DetailView):
    context_object_name = 'user'
    queryset = CustomUser.objects.all()
    template_name = 'profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_profile"] = self.get_object() == self.request.user
        return context
    

# * profile edit view
class EditProfileView(generic.TemplateView):
    template_name='profile_settings.html'
    def get_object(self):
        return self.request.user
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        # allow only profile owner
        if request.user != self.get_object():
            raise PermissionDenied('you dont have permmision to view this page')
        return super().get(request, *args, **kwargs)
    
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        # update user profile here
        obj = self.get_object()
        
        # get new data
        username = request.POST['username']
        image = request.FILES.get('image')
        bio = request.POST['bio']
        email = request.POST['email']
        if image is not None:
            obj.profile_image = image
        if ' ' in username:
            messages.info(request,'invalid character in username')
            return redirect('update_profile')
            
        if not CustomUser.objects.filter(username=username).exists():
            obj.username = username

        obj.bio = bio
        obj.email = email
        
        obj.save()
        return redirect('profile' ,username = request.user.username)
    
    
#todo: Add password recovery view here
def redirect_to_homepage(request):
    x = request.session['recent_chats']
    print(x)
    return redirect('index')

