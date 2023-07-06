# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm
from .models import CustomUser, Groups, Messages,RecentMsg


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
admin.site.register(Groups)
admin.site.register(RecentMsg)