from django.urls import path
from .views import *

app_name = 'about'

urlpatterns = [
    path('team/',TeamView.as_view(),name='team'),
    path('codersource/',AboutView.as_view(),name='codersource'),

]