from django.db import models
from ckeditor.fields import RichTextField
import uuid
from datetime import datetime
from django.utils.timezone import now
from users.models import Profile

class Ads(models.Model):
    user = models.CharField(max_length=20)
    name = models.CharField('name',max_length=15)
    image =  models.ImageField(upload_to='ad_images')
    reg_date = models.DateField(default=now)
    uid = models.UUIDField(default=uuid.uuid4,editable=False)
    body = RichTextField(config_name='default')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Advertisement'
        verbose_name_plural = 'Advertisements'

class Post(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='post_images')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    source = models.FileField(upload_to='sources')
    caption = models.TextField()
    created_at = models.DateField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class LikedPost(models.Model):
    post_id = models.CharField(max_length=150)
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class BanList(models.Model):
    user = models.CharField('banned user',max_length=50)

class Questions(models.Model):
    body = models.CharField(max_length=25)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    uid = models.UUIDField(default=uuid.uuid4,editable=False,unique=True,primary_key=True)
    is_seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.user.user.get_username()
    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        
