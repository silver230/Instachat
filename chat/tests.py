from django.test import TestCase
from django.contrib.auth.models import User
from .models import Posts,Profile,Comments,Likes,Follow
# Create your tests here.



class UserTest(TestCase):
    def setUp(self):
        self.user=User(username='dk',first_name='d',last_name='k',email='dk@gmail.com')
    
    def test_instance(self):
        self.assertTrue(isinstance(self.user,User))
    
    def test_data(self):
        self.assertTrue(self.user.username,"mj")
        self.assertTrue(self.user.first_name,"d")
        self.assertTrue(self.user.last_name,'k')
        self.assertTrue(self.user.email,'mj@gmail.com')
    
    def test_save(self):
        self.user.save()
        users = User.objects.all()
        self.assertTrue(len(users)>0)
    
    def test_delete(self):
        user = User.objects.filter(id=1)
        user.delete()
        users = User.objects.all()
        self.assertTrue(len(users)==0)

class ProfileTest(TestCase):
    def setUp(self):
        self.new_user=User(username='aa',first_name='a',last_name='a',email='a@gmail.com')
        self.new_user.save()
        self.new_profile=Profile(user=self.new_user,bio='wueh')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_profile,Profile))
    
    def test_data(self):
        self.assertTrue(self.new_profile.bio,"wuehh")
        self.assertTrue(self.new_profile.user,self.new_user)

    def test_save(self):
        self.new_profile.save()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles)>0)
    
    def test_delete(self):
        profile = Profile.objects.filter(id=1)
        profile.delete()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles)==0)

    
    def test_edit_profile(self):
        self.new_profile.save()
        self.update_profile = Profile.objects.filter(bio='wueh').update(bio = 'aaabbbcccddd')
        self.updated_profile = Profile.objects.get(bio='aaabbbcccddd')
        self.assertTrue(self.updated_profile.bio,'aaabbbcccddd')


 
