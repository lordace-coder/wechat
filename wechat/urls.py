
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from chat.views import redirect_to_homepage



urlpatterns = [
    path('',redirect_to_homepage),
    path('chat/',include('chat.urls')),
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
