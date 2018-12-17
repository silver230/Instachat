from django.shortcuts import render,redirect
from . forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Posts,Profile,Follow
from .forms import NewPostForm,Prof,Comments,UserForm,ProfileForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage,message
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import gettext as _




# Create your views here
# @login_required(login_url='/accounts/login/')
def index(request):
    post = Posts.objects.all()
    comm = Comments()
    # like = Likes()
    return render(request,'index.html', {"post":post,"comm":comm})

def update_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
    user.save()
    return render(request,"profiles/profile.html",{"user":user,"user_id":user_id})


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,_('Your profile was successfully updated!'))
            return redirect('settings:profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })       
  
def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username,email=email, password=raw_password)
            profile = Profile(user=user)
            profile.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your instagram account.'
            message = render_to_string('email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

            login(request,user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration_form.html', {'form': form})


 

 
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.<a href="/auth/login">Login</a>')
    else:
        return HttpResponse('Activation link is invalid!')

# @login_required(login_url='/accounts/login/')
def post(request,post_id):
    try:
        post = Posts.objects.get(id = post_id)
    except Posts.DoesNotExist:
        raise Http404()
    return render(request,"all-chats/post.html", {"post":post})

# @login_required(login_url='/accounts/login/')
def new_post(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.editor = current_user
            post.save()
        return redirect('index')

    else:
        form = NewPostForm()
    return render(request, 'new_post.html', {"form": form})  

 
 

    return render(request, 'profile/edit_profile.html', {'form':form})
@login_required(login_url='/auth/login')
def comment(request,id):
    post = Posts.objects.get(id=id)
    if request.method == 'POST':
        comm=Comments(request.POST)
        if comm.is_valid():
            comment=comm.save(commit=False)
            comment.user = request.user
            comment.post=post
            comment.save()
            return redirect('index')
    return redirect('index')

def search_results(request):
    
    if 'user' in request.GET and request.GET["user"]:
        search_item = request.GET.get("user")
        searched_users = User.objects.filter(username=search_item)
        print(searched_users)
        message = f"{search_item}"
        return render(request, 'search.html',{"message":message,"users": searched_users})
    else:
        message = "You haven't searched for any user"
        return render(request, 'search.html',{"message":message})


     