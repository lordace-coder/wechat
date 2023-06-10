from django.contrib import admin
from .models import Messages
# Register your models here.
from django.contrib import admin
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'additional info',
            {
                'fields':(
                    'profile_image',
                    'bio'
                )
            }
        )
    )
    
admin.site.register(CustomUser,CustomUserAdmin)

admin.site.register(Messages)