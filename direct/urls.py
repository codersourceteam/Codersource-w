from django.urls import path
from .views import *
app_name = 'direct'

urlpatterns = [
    path('<str:username>',DirectView.as_view(),name='direct'),
    path('inbox/<str:id>',InboxView.as_view(),name='inbox'),
    path('send/<str:id>/<str:sender>/<str:receiver>',SendMessage.as_view(),name='send'),
    path('create/<str:receiver>',CreateChatView.as_view(),name='create')
]