from typing import Iterable, Optional
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse,reverse_lazy


# Create your models here.
class Groups(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name




class CustomUser(AbstractUser):
    profile_image = models.ImageField(blank=True,null=True,upload_to='images/profile_images',default='default_img.png')

    email = models.CharField(max_length=200)

    bio = models.TextField(_("bio"), blank=True)

    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name=_("groups"),
        blank=True,
        related_name="custom_users"
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name=_("user permissions"),
        blank=True,
        related_name="custom_users"
    )

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.username
    
    
    def get_image_url(self):
        url = f'{self.profile_image}'
        print(self.profile_image)
        if 'images/profile_image' not in url:
            url = None
        # print(self.get_absolute_url())
        return url


class Messages(models.Model):
    group = models.ForeignKey(Groups,on_delete=models.SET_NULL,blank=True,null=True)
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    reciever = models.CharField(max_length=180,blank=True,null = True)
    message = models.TextField()
    time = models.DateTimeField(auto_now=True)
    
    
    def save(self, *args, **kwargs) -> None:
        if self.group:
            self.reciever = self.group.name
        return super().save(*args, **kwargs)    
