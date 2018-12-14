from django.shortcuts import render,redirect
from . forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Posts,Comments,Likes

# Create your views here
# @login_required(login_url='/auth/login')
def index(request):
    post = Posts.objects.all()
    comm = Comments()
    like = Likes()
    return render(request,'index.html', {"post":post,"like":like,"comm":comm})




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
    return render(request, 'singup_form.html', {'form': form})