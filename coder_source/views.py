from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def handler(request,exception):
    return render(request,'error/404.html')

@login_required
def handler1(request):
    return render(request,'error/500.html')