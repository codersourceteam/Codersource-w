from django.db import models
from users.models import Profile
from ckeditor.fields import RichTextField
class User(Profile):
    is_premium = models.BooleanField(default=False)
    files_uploaded = models.PositiveIntegerField()

class Document(models.Model):
    name = models.CharField(max_length=25,default='document')
    signature = RichTextField()
    file = models.FileField(upload_to='document_files')
    def __str__(self):
        return self.name
