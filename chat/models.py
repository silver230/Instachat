from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from django.db.models.signals import post_save
from django.dispatch import receiver
from tinymce.models import HTMLField
# Create your models here

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    profimage = models.ImageField(upload_to='posts')
    birth_date = models.DateField(null=True, blank=True)


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
            instance.profile.save()

    def __str__(self):
        return self.bio

class Posts(models.Model):
    id = models.primary_key=True
    caption = models.CharField(max_length=250)
    user=models.ManyToManyField(User,related_name='post')
    image = models.ImageField(upload_to='posts')
    postedon = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile,null=True)
    
    
    def __str__(self):
        return self.caption

    class Meta:
        ordering = ['-id']
    
    @classmethod
    def save_post(self):
        self.save()
    @classmethod
    def get_posts(cls):
         posts = cls.objects.all()
         return posts
    @classmethod
    def delete_post(self):
        self.delete()
    
    def save_image(self):
        self.save()

    @classmethod
    def delete_image_by_id(cls, id):
        pictures = cls.objects.filter(pk=id)
        pictures.delete()

    @classmethod
    def get_image_by_id(cls, id):
        pictures = cls.objects.get(pk=id)
        return pictures


class Comments(models.Model):
    user = models.ForeignKey(User)
    post=models.ForeignKey(Posts,related_name='comments')
    comment=models.CharField(max_length=200)

class Likes(models.Model):
    user = models.OneToOneField(User,related_name='l_user')
    post=models.ForeignKey(Posts,related_name='likes')
    like=models.CharField(max_length=3,default='1')
     


class Follow(models.Model):
    users=models.ManyToManyField(User,related_name='follow')
    current_user=models.ForeignKey(User,related_name='c_user',null=True)

    @classmethod
    def follow(cls,current_user,new):
        friends,created=cls.objects.get_or_create(current_user=current_user)
        friends.users.add(new)
    
    @classmethod
    def unfollow(cls,current_user,new):
        friends,created=cls.objects.get_or_create(current_user=current_user)
        friends.users.remove(new)
