from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Posts,Comments,Profile,Likes



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ['first_name', 'last_name','email', 'password1', 'password2', ]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio','location','birth_date','profimage')        

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Posts
        exclude = ['user','postedon']
        fields = ['caption','image']
       
class Prof(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=[]
        fields=['bio']


class Comments(forms.ModelForm):
    class Meta:
        model=Comments
        exclude=[]
        fields=['comment']

class Likes(forms.ModelForm):
    class Meta:
        model=Likes
        exclude=[]
        fields=[]

# class NewPostForm(forms.ModelForm):
#     class Meta:
#         model =  Posts
#         exclude = ['pub_date']
#         fields =[]
 