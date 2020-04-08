from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from .models import Message, Group
from .models import Profile
import json

def temp(request, sb_id):
    if sb_id > request.user.id:
        room_name = str(request.user.id) + '_' + str(sb_id)
    else:
        room_name = str(sb_id) + '_' + str(request.user.id)

    try:
        group = Group.objects.get(name=room_name)
    except: 
        par1 = User.objects.get(id=sb_id)
        profile1 = Profile.objects.get(user=par1)
        par2 = User.objects.get(id=request.user.id)
        profile2 = Profile.objects.get(user=par2)
        group = Group(name=room_name)
        group.save()
        group.participants.add(par1, par2)
        histr = profile2.nickname +"님과 " + profile1.nickname + "님의 채팅방이 개설되었습니다!"
        msg = Message(sender=par2, recipient=par1, room=group, content=histr)
        msg.save()

    return redirect('room', room_name=group)

def chat_list(request):
    groups = Group.objects.all()
    msglist = []
    for group in groups:
        if request.user in group.participants.all():
            msg = Message.objects.filter(room=group)[0]
            msglist.append(msg)
    if len(msglist) == 0:
        msglist = None
    return render(request, 'chat_list.html', {'msglist':msglist})

def room(request, room_name):
    group = room_name.split('_')
    if str(request.user.id) not in group:
        content="<script type='text/javascript'>alert('채팅방에 입장하실 수 없습니다.');history.back();</script>"
        return HttpResponse(content)
    group.remove(str(request.user.id))
    other = User.objects.get(id=group[0])
    group = Group.objects.get(name=room_name)
    if request.method=='POST':
        content = request.POST['message']
        sender = request.user
        msg = Message(sender=sender, recipient=other, room=group, content=content)
        msg.save()

    name = request.user.username
    messages = Message.objects.filter(room=group)
    messages = messages.order_by('sentAt')
    nick = other.profile.nickname
    if other.profile.profileimg:
        other = other.profile.profileimg.url
    else:
        other = "nan"

    return render(request, 'room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'name' : mark_safe(json.dumps(name)),
        'messages': messages,
        'other': mark_safe(json.dumps(other)),
        'nick' : mark_safe(json.dumps(nick)),
    })