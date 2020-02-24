from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .models import Profile
from bookmap.models import BookStore, Scrap, Stamp, Tag
import os
from urllib.parse import urlparse
import requests
from django.core.files.base import ContentFile
from django.db.models import Q


# Create your views here.
def home(request):
    tf = False
    if request.user.is_authenticated:
        user = request.user
        try:
            profile=Profile.objects.get(user=user)
        except:
            if not user.is_superuser:
                tf = True
    #처음 소셜로그인해서 프로필 없을경우만 tf=True
    if tf == True:
        email = user.email
        nick = user.username
        profile = Profile(user=user, email=email, nickname=nick)
        profile.save()
        return render(request, 'social.html')
    #여기부터 추천
    else:
        try:
            tag_set = request.user.profile.tag_set.all()
            stores = BookStore.objects.all()
            arr = []
            for store in stores:
                temp = []
                temp.append(store.name)
                s1 = set(store.tag_set.all()) # 책방 태그 집합
                s2 = set(tag_set) # 내 취향 집합
                if s1 & s2:
                    temp.append(len(s1 & s2)) # 교집합 개수
                    arr.append(temp)
            arr.sort(key=lambda x:x[1])
            arr.reverse()
            arr = arr[:10]
            q = Q()
            for s in arr:
                q.add(Q(name=s[0]), q.OR)
            stores = BookStore.objects.filter(q).order_by('?')[:5]

            # 내가 고른 태그 중 랜덤으로 추천
            '''
            tag_set = request.user.profile.tag_set.all()
            tag = tag_set.order_by('?')[0]
            stores = BookStore.objects.all()
            q = Q()
            for store in stores:
                if tag in store.tag_set.all():
                    q.add(Q(name=store.name), q.OR)
            stores = BookStore.objects.filter(q).order_by('?')[:4]
            '''
        except:
            stores = '' #태그 없으면 로그인 안한 사람이랑 같은 로직으로 ㄱㄱ
            
        return render(request, 'home.html', {'stores':stores})

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
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('tag')
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
    return render(request, 'signup.html')

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
    return render(request,'mypage.html', {
                        'scraps':scraps, 
                        'stamp':mystamp,
                        'level':level,
                        'next':next_level,
                        'more':more,
                        'user':user,
                        'profile': profile,
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
    return redirect('tag')

def tag(request):
    tag = Tag.objects.all().order_by('?')
    return render(request, 'tag.html', {'tag': tag,})
    
def tag_count(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    return HttpResponse(str(tag.tag_count()))

def pro_tag(request):
    tag = request.POST.getlist('tag')
    profile = Profile.objects.get(user=request.user)
    for t in tag:
        temp=Tag.objects.get(title=t)
        profile.tag_set.add(temp)
    return redirect('home')

def mytag(request):
    mytag = request.user.profile.tag_set.all()
    alltag = Tag.objects.all()
    alltag = alltag.difference(mytag)
    return render(request, 'mytag.html',{'alltag':alltag, 'mytag':mytag})
