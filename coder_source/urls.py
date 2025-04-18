"""coder_source URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings
admin.autodiscover()
from .views import *
urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),

    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

    path('ttf/toptallent/', admin.site.urls),

    path('',include('core.urls')),

    path('auth/',include('users.urls')),
    path('verify/',include('verification.urls')),
    path('about/',include('about.urls')),
    path('direct/',include('direct.urls')),
    path('delete/',include('delete.urls')),
    path('ad/',include('advert.urls')),
    path('search/',include('search.urls')),
    path('ttf/modder/',include('moderator.urls')),
    path('api/',include('api.urls')),
    path('edit/',include('edit.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

handler404 = handler
handler500 = handler1
