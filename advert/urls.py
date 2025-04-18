from django.urls import path
from .views import *

app_name = 'advert'

urlpatterns = [
    path('detail/<str:id>',DetailView.as_view(),name='detail'),
    path('comment/<str:id>',CommentView.as_view(),name='comment')
]