from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    # auth views
    path('login/',views.login,name="login"),
    path('signup/',views.signup,name="signup"),
    path('logout',views.logout,name="logout"),
    
    
    path('', views.index, name='index'),
    path('<int:userId>', views.room, name='room'),
    path('<str:groupName>', views.group_room, name='group_room'),
    path('messages/<str:roomName>',views.get_messages,name="messages"),

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
