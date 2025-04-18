from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path('cmatrix',cmatrix,name='cmatrix'),
    path('upload',UploadView.as_view(),name='upload'),
    path('like/<str:id>',like_post,name='like'),
    path('detail/<str:id>',DetailView.as_view(),name='detail'),
    path('add/question',AddQuestion.as_view(),name='detail'),
    path('<str:username>/',ProfileView.as_view(),name='profile'),

    
]