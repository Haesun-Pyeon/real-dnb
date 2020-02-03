from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from .models import Message, Group
import json

def index(request):
    return render(request, 'index.html', {})

def chat_list(request):
    groups = Group.objects.all()
    msglist = []
    for group in groups:
        if request.user in group.participants.all():
            msg = Message.objects.filter(room=group)[0]
            msglist.append(msg)
    return render(request, 'chat_list.html', {'msglist':msglist})

def room(request, room_name):
    try:
        group = Group.objects.get(name=room_name)
    except:
        group = Group(name=room_name)
        group.save()
    if request.method=='POST':
        content = request.POST['message']
        sender = request.user
        msg = Message(sender=sender, room=group, content=content)
        msg.save()
    name = request.user.username
    messages = Message.objects.filter(room=group)
    messages = messages.order_by('sentAt')
    return render(request, 'room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'name' : mark_safe(json.dumps(name)),
        'messages': messages,
    })