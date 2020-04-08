from django.db import models
from django.contrib.auth.models import User
from main.models import *

# Create your models here.

class BookStore(models.Model):
    bookstore_id = models.AutoField(primary_key=True)
    name = models.CharField('책방이름',max_length=20)
    addr = models.TextField('책방주소',unique=True)
    phone_number = models.CharField('전화번호', blank=True, max_length=15, null=True)
    site = models.URLField('웹사이트',null=True, blank=True)
    img = models.URLField(null=True, blank=True)
    insta = models.CharField('인스타그램',null=True, blank=True, max_length=50)
    email = models.EmailField('이메일', null=True, blank=True)
    openhour = models.TextField('영업시간',null=True, blank=True)
    users = models.ManyToManyField(User, through='Scrap', related_name='%(app_label)s_%(class)s_related')
    thema_set = models.ManyToManyField('Thema', blank=True)
    tag_set = models.ManyToManyField('Tag', blank=True)

    class Meta:
        ordering = ['bookstore_id']

    def __str__(self):
        return self.name

    def like_count(self):
        return Scrap.objects.filter(store=self).count()

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('storedetail', args=[str(self.pk)])

class Tag(models.Model):
    title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.title
    
    def tag_count(self):
        store = BookStore.objects.all()
        count = 0
        for s in store:
            if self in s.tag_set.all():
                count += 1
        return count

class Thema(models.Model):
    title = models.CharField(max_length=30, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    description = models.TextField()
    img = models.ImageField(upload_to='thema/', null=True, blank=True)
    private = models.BooleanField(default=False)
    like = models.ManyToManyField(User, related_name='like')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return '%s, %s' % (self.title, self.user)
    
    def total_like(self):
        return self.like.count()

class Scrap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(BookStore, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s, %s' %(self.user,self.store)

class Review(models.Model):
    store = models.ForeignKey(BookStore, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    content = models.CharField(max_length=200)
    star = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s, %s' %(self.store, self.content[:30])

class Stamp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(BookStore, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    count = models.IntegerField(default=1)

    def __str__(self):
        return '%s, %s' %(self.user,self.store)