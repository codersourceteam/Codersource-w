from django.shortcuts import render,redirect
from django.views import View
from core.models import Ads
from .models import Comment
from users.models import Profile

class DetailView(View):
    def get(self,request,id):
        ad = Ads.objects.get(uid=id)
        comment = Comment.objects.filter(ad=id)
        profile = Profile.objects.get(user=request.user)


        context = {
            'ad':ad,
            'comment':comment,
            'prf':profile,
        }

        return render(request,'advertisement/detail.html',context)
    

class CommentView(View):
    def post(self,request,id):
        if request.user.is_authenticated:
            prf = Profile.objects.get(user=request.user)
            value = request.POST['message']
            Comment.objects.create(user=prf,comment=value,ad=id)
            return redirect(f'/ad/detail/{id}')
        else:
            return redirect('users:login')