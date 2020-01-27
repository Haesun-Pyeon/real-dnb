from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10) 
    email = models.EmailField()
    level = models.IntegerField(default=1)
    profileimg = models.ImageField(upload_to='profileimg/', blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def stampcount(self):
        mystamp = 0
        for i in self.user.stamp_set.all():
            mystamp += i.count
        return mystamp