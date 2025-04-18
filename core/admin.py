from django.contrib import admin

from users.models import *
from .models import *
from verification.models import VerReq

admin.site.register(FollowersCount)
admin.site.register(Request)
admin.site.register(Profile)
admin.site.register(BanList)
admin.site.register(Post)
admin.site.register(Ads)
admin.site.register(VerReq)
admin.site.register(LikedPost)
admin.site.register(Questions)