from django.urls import path
from .views import *

app_name = 'verification'

urlpatterns = [
    path('<str:user>/',VerificationView.as_view(),name='ver'),
    path('proccess/unverify/',UnverifyProccess.as_view(),name='proccess'),
    path('cancel/verification',Unverify.as_view(),name='unverify'),
]