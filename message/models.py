from django.db import models
from django.contrib.auth.models import User
from main.models import Profile
from django.utils import timezone

class Group(models.Model):
    name = models.CharField(max_length=30, unique=True)
    participants = models.ManyToManyField(User, related_name='participants')

    def __str__(self):
        return self.name

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="message_sender", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="message_receiver", on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Group, related_name="chat_group", on_delete=models.CASCADE)
    sentAt = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=300)
    #isRead = models.BooleanField(default=False)

    objects = models.Manager()

    def save(self, **kwargs):
        if not self.id:
            self.sentAt = timezone.now()
        super(Message, self).save(**kwargs)

    class Meta:
        ordering = ['-sentAt']

    def __str__(self):
        return '%s, %s' %(self.sender, self.content)
    
    def summary(self):
        return self.content[:17]

    def senderProfile(self):
        who = Profile.objects.get(user=self.sender)
        return who