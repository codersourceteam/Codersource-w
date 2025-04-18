from django.urls import path
from .views import *

app_name = 'moderator'

urlpatterns = [


    path('',IndexView.as_view(),name='index'),
    path('verification/<str:id>',EditVer.as_view(),name='verification'),
    path('verify/<str:id>',Verify.as_view(),name='verify'),
    path('post/<str:post>',EditPost.as_view(),name='post'),
    path('delete/<str:post>',DeletePost.as_view(),name='deletepost'),
    path('answer/<str:id>',Answer.as_view(),name='answer'),


]