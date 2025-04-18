from django.urls import path
from .views import *

app_name = 'edit'

urlpatterns = [

    path('post/<str:id>',EditPostView.as_view(),name='post')

]