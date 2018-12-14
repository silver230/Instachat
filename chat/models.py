from django.db import models

# Create your models here.
 from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from tinymce.models import HTMLField
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    profimage =  models.ImageField(upload_to='images')
    bio = HTMLField(max_length=500)

    
    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()
    
    def __str__(self):
        return self.user.username

 