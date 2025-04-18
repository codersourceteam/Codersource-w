from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('login/',LogInView.as_view(),name='login'),
    path('signup/',SignUpView.as_view(),name='signup'),
    path('forget',ForgotView.as_view(),name='forgot'),
    path('settings/',SettingsView.as_view(),name='settings'),
    path('logout/',logout_view,name='logout'),
    path('follow/<str:usr>',FollowView.as_view(),name='follow'),
    path('changepass/<str:id>/',ChangeView.as_view(),name='change'),
    path('followers/<str:username>/',FollowersView.as_view(),name='followers'),
    path('verify/<str:id>/',VerifyView.as_view(),name='activate'),
    path('all/',AllUsers.as_view(),name='all'),
    path('comment/<str:id>/',AddComment,name='comment'),
    path('changepas/',ChangePassword.as_view(),name='changepas'),
]