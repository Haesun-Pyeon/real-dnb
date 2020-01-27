from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .models import Profile
from bookmap.models import BookStore, Scrap, Stamp
from culture.models import Comment ##
import os
from urllib.parse import urlparse
import requests
from django.core.files.base import ContentFile


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            profile=Profile.objects.get(user=user)
            return render(request, 'home.html')
        except:
            if request.user.is_superuser:
                return render(request, 'home.html')
            email = user.email
            nick = user.username
            profile = Profile(user=user, email=email, nickname=nick)
            profile.save()
            return render(request, 'social.html')
    else:
        return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        # User has info and wants an account now! 즉 [signup!]버튼을 눌렀을 때 일어나는 일
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                content="<script type='text/javascript'>alert('이미 존재하는 아이디입니다.');history.back();</script>"
                return HttpResponse(content)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'])
                nickname=request.POST['nickname']
                email = request.POST['email']
                profile = Profile(user=user, nickname=nickname, email=email)
                profile.save()
                auth.login(request, user)
                return redirect('home')
        else:
            content="<script type='text/javascript'>alert('비밀번호가 일치하지 않습니다.');history.back();</script>"
            return HttpResponse(content)
    else:
       # User wants to enter info --> 유저가 정보를 입력하고 있는 중임.
        return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None: #사용자 정보를 알맞게 입력한 경우
            auth.login(request, user)
            return redirect('home')
        else:  #잘못 입력한경우
            try:
                user = User.objects.get(username=username)
                if not check_password(password, user.password):
                    content="<script type='text/javascript'>alert('비밀번호가 일치하지 않습니다.');history.back();</script>"
                    return HttpResponse(content)
            except User.DoesNotExist:
                content="<script type='text/javascript'>alert('아이디가 존재하지 않습니다.');history.back();</script>"
                return HttpResponse(content)
    else:
        return render(request, 'login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    return render(request, 'main/signup.html')

def del_user(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if profile.profileimg:
        os.remove(profile.profileimg.path)
    user.delete()
    auth.logout(request)
    return render(request, 'home.html')
    
def user_change(request):
    if request.method == "POST":
        user = request.user
        try:
            new_img = request.FILES['img_file']
            profile = Profile.objects.get(user=user)
            if profile.profileimg:
                os.remove(profile.profileimg.path)
            profile.profileimg = new_img
            profile.save()
        except:
            pass
        new_pwd = request.POST.get("password1")
        pwd_confirm = request.POST.get("password2")
        if new_pwd == "":
            if (new_img):
                message = "프로필 사진이 성공적으로 변경되었습니다."
                return render(request,'popup.html',{'message':message})
            else:
                return redirect('mypage')
        if new_pwd == pwd_confirm:
            user.set_password(new_pwd)
            user.save()
            auth.login(request, user)
            message = "비밀번호가 성공적으로 변경되었습니다."
            return render(request,'popup.html',{'message':message})
        else:
            message = "비밀번호가 일치하지 않습니다."
            return render(request, 'popup.html', {'message': message})
            
def mypage(request):
    user = request.user
    if user.is_superuser:
        return render(request, 'home.html')
    else:
        profile = Profile.objects.get(user=request.user)
        mystamp = profile.stampcount()
        level = profile.level
        if level==3:
            next_level = None
        else:
            next_level = level + 1
        more = level*10-mystamp
    scraps = Scrap.objects.filter(user=request.user)
    comments = Comment.objects.filter(user=request.user) #컬쳐 바꾸면 빼기
    return render(request,'mypage.html', {
                        'scraps':scraps, 
                        'stamp':mystamp,
                        'level':level,
                        'next':next_level,
                        'more':more,
                        'user':user,
                        'profile': profile,
                        'commnets': comments,
                        })

def test(request):
    return render(request, 'test.html')

def social(request):
    if request.method == 'POST':
        img_url = request.POST['img_url']
        user = request.user
        profile = Profile.objects.get(user=user)
        name = urlparse(img_url).path.split('/')[-1]
        response = requests.get(img_url)
        if response.status_code == 200:
            profile.profileimg.save(name, ContentFile(response.content), save=True)
    return redirect('home')
