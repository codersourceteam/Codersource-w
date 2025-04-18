from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
import uuid
from datetime import datetime

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.PositiveIntegerField()
    uid = models.UUIDField(default=uuid.uuid4,editable=False)
    name = models.CharField('Name',max_length=20)
    likes = models.IntegerField(default=0)
    bio = RichTextField(default='none')
    reg_date = models.CharField(max_length=26,default=datetime.now(),editable=False)
    profileimg = models.ImageField(upload_to='profile_images', default='1.png')
    is_online = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_team_member = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class FollowersCount(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='followers')
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.user.get_username()

class Request(models.Model):
    user = models.CharField(max_length=20)
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    email = models.EmailField()
    code = models.PositiveIntegerField()

    def __str__(self):
        return self.user

class ViewsCount(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post_id = models.UUIDField()

    def __str__(self):
        return self.user.get_username()

    class Meta:
        verbose_name = 'View'
        verbose_name_plural = 'Views'

class Comment(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    post = models.UUIDField()
    comment = models.TextField()
    ctime = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    uid = models.UUIDField(verbose_name='uid',default=uuid.uuid4,editable=False)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.user.get_username()

    class Meta:

        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

