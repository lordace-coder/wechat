
from django.contrib import admin
from django.urls import path,include
from chat.views import redirect_to_homepage


urlpatterns = [
    path('',redirect_to_homepage),
    path('chat/',include('chat.urls')),
    path('admin/', admin.site.urls),
]
