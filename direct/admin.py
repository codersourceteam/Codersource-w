from django.contrib import admin
from .models import *

admin.site.register(Message)
admin.site.register(Inbox)
admin.site.register(UnreadMessage)