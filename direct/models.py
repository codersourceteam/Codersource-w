from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from users.models import Profile
import uuid

class Inbox(models.Model):
    owner = models.ForeignKey(Profile,on_delete=models.PROTECT,related_name='owner')
    user = models.ForeignKey(Profile,on_delete=models.PROTECT)
    uid = models.UUIDField(default=uuid.uuid4,editable=False)
    unread = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.owner.user.get_username()
    class Meta:
        verbose_name = 'Inbox'
        verbose_name_plural = 'Inboxes'


class Message(models.Model):
    inbox = models.ForeignKey(Inbox,on_delete=models.PROTECT)
    sender = models.ForeignKey(Profile,on_delete=models.PROTECT,related_name='sender')
    receiver = models.ForeignKey(Profile,on_delete=models.PROTECT,related_name='receiver')
    uid = models.UUIDField(default=uuid.uuid4,editable=False)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.inbox.owner.user.get_username()
    
    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'


class UnreadMessage(models.Model):
    message = models.ForeignKey(Message,on_delete=models.CASCADE)