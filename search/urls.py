from django.urls import path
from .views import *

app_name = 'search'


urlpatterns = [

    path('post/',SearchPost.as_view(),name='post')

]