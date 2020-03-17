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

import boto3

def s3_delete(key):
    s3 = boto3.resource('s3')
    bucket_name = os.environ.get("AWS_STORAGE_BUCKET_NAME")
    path='media/'+str(key)
    s3.Object(bucket_name, path).delete()

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
        return render(request, 'temp.html', {'tf': tf})
    #여기부터 추천
    else:
        try:
            weight={} #태그별 가중치
            tag_set = request.user.profile.tag_set.all()
            arr = []
            scrap = Scrap.objects.filter(user=request.user)  #좋아요한 책방
            if (tag_set.count() == 0) and (scrap.count() == 0):
                raise ValueError
            if (scrap.count() != 0):
                like_pk=[]
                for s in scrap:
                    like_list = s.store.tag_set.all().values_list('title', flat=True)
                    like_pk.append(s.store.bookstore_id)
                    for l in like_list:
                        if l in weight.keys():
                            weight[l] += 0.1
                        else:
                            weight[l] = 0.1
                stores = BookStore.objects.exclude(bookstore_id__in=like_pk)
            else:
                stores = BookStore.objects.all()
            if (tag_set.count() != 0):
                for t in tag_set:
                    if t.title in weight.keys():
                        weight[t.title] += 1
                    else:
                        weight[t.title] = 1
            for store in stores:
                store_weight = 0 #그 가게의 최종가중치
                temp = []
                temp.append(store.name)
                for t in store.tag_set.all():
                    if t.title in weight.keys():
                        store_weight += weight[t.title]
                temp.append(round(store_weight,1))
                arr.append(temp)
            arr.sort(key=lambda x:x[1])
            arr.reverse()
            arr = arr[:15]
            q = Q()
            for a in arr:
                q.add(Q(name=a[0]), q.OR)
            stores = BookStore.objects.filter(q).order_by('?')[:5]
            return render(request, 'home.html', {'stores':stores,})
        except: # 추천 못하는경우 현위치기반
            tf = None
            return render(request, 'temp.html', {'tf': tf})

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
        # os.remove(profile.profileimg.path)
        s3_delete(profile.profileimg)
    user.delete()
    auth.logout(request)
    return redirect('home')
    
def user_change(request):
    if request.method == "POST":
        user = request.user
        try:
            new_img = request.FILES['img_file']
            profile = Profile.objects.get(user=user)
            # if profile.profileimg:
                # os.remove(profile.profileimg.path)
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

def tag_change(request):
    mytag = request.POST.getlist('mytag')
    profile = Profile.objects.get(user=request.user)
    profile.tag_set.clear()
    for t in mytag:
        temp = Tag.objects.get(title=t)
        profile.tag_set.add(temp)
    return redirect('mytag')

def non_log(request, addr):
    if addr == '123': #현위치 못받아올때는 랜덤 5개
        stores = BookStore.objects.all().order_by('?')[:5]
        return render(request, 'home.html', {'stores': stores,})
    else:
        address = addr.split()
        if len(address[0]) > 2:
            address[0] = address[0][:2]
        bookstore = BookStore.objects.filter(addr__startswith=address[0], addr__contains=address[1])
        if len(bookstore) <= 5:
            bookstore = BookStore.objects.filter(addr__startswith=address[0])
            stores = bookstore.order_by('?')
        else:
            stores = bookstore.order_by('?')[:5]
        return render(request, 'home.html', {'stores':stores,})