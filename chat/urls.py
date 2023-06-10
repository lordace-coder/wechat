from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:userId>/', views.room, name='room'),
    path('messages/<str:roomName>',views.get_messages,name="messages"),
    
    # auth views
    path('login/',views.login,name="login"),
    path('signup/',views.signup,name="signup"),
    path('logout',views.logout,name="logout"),
]