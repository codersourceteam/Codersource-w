from django.shortcuts import render,redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .check import check_login
from users.models import Profile


class VerificationView(View):
    def get(self,request,user):
        rus = request.user
        if request.user.is_authenticated:
            if User.objects.filter(username=user).exists():
                if user == rus.username:
                    p = Profile.objects.get(user__username=user)
                    print(p)
                    if not p.is_verified == True:
                        if VerReq.objects.filter(user=user).exists():
                            messages.info(request,"You've already requested to Verify Your account!")
                            return redirect('core:index')
                        else:
                            prf = Profile.objects.get(user=request.user)
                            context = {
                                'prf':prf
                            }

                            return render(request,'verification/verification.html',context) 
                    else:
                        messages.info(request,"This Account already verified !")
                        return redirect('core:index')
                else:
                    messages.info(request,"This Account isn't yours")
                    return redirect('core:index')
            else:
                messages.info(request,"User Not Found")
                return redirect('core:index')
        else:
            return redirect('users:login')

    def post(self,request,user):
        if request.user.is_authenticated:
            url = request.POST['url']
            q = request.POST['query']
            email = request.POST['email']
            VerReq.objects.create(user=user,url=url,query=q,email=email)
            messages.info(request,"Requested Wait for mail !")
            return redirect('core:index')
        else:
            return redirect('users:login')
        


class UnverifyProccess(View):
    def get(self,request):
        check_login(request.user)
        prf = Profile.objects.get(user=request.user)
        if prf.is_verified:
            prf = Profile.objects.get(user=request.user)
            context = {
                'prf':prf
            }
            return render(request,'verification/unverify.html',context)
        else:
            return redirect('core:index')
        
class Unverify(UnverifyProccess):
    def get(self,request):
        check_login(request.user)
        prf = Profile.objects.get(user=request.user)
        if prf.is_verified:
            prf.is_verified = False
            prf.save()
            messages.info(request,"Your Profile Successfully Unverified")
            return redirect('core:index')
        else:
            messages.info(request,"You aren't verified your profile! Please request for verification!")
            return redirect('core:index')
        
