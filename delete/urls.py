from django.urls import path
from .views import *

app_name = 'delete'

urlpatterns = [
    path('comment/<str:id>/<str:post>',DeleteComment,name='comment'),
    path('post/<str:id>',DeletePost,name='post'),
]