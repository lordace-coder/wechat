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
    path('groups/<str:groupName>', views.group_room, name='group_room'),
    path('messages/<str:roomName>',views.get_messages,name="messages"),
    path('groups/',views.GroupChatView.as_view(),name='groups'),
    path('users/',views.ListUsersView.as_view(),name='all_users'),
    path('profile/<slug:username>',views.ProfileDetailView.as_view(),name='profile'),
    path('updateProfile/',views.EditProfileView.as_view(),name='update_profile'),

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
