from django.db import models
import uuid

class VerReq(models.Model):
    uid = models.UUIDField(default=uuid.uuid4,editable=False)
    user = models.CharField(max_length=20)
    query = models.TextField()
    url = models.URLField()
    email = models.EmailField()

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'Verification Request'
        verbose_name_plural = 'Verification Requests'
