from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse,reverse_lazy


# Create your models here.






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
    



class Messages(models.Model):
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    reciever = models.CharField(max_length=180,default="lordace_lordace2")
    message = models.TextField()
    time = models.DateTimeField(auto_now=True)