from django.db import models
from users.models import Profile
import uuid
class Comment(models.Model):
    ad = models.UUIDField()
    comment = models.TextField()
    user = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='ad_comments')
    uid = models.UUIDField(default=uuid.uuid4,editable=False)

    def __str__(self):
        return self.user.user.get_username()
    
    class Meta:
        verbose_name = 'Ad Comment'
        verbose_name_plural = 'Ad Comments'
