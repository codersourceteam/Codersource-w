from django.shortcuts import render,redirect
from django.views import View
from users.models import Profile
from django.contrib.auth.models import User
from users.models import FollowersCount

class TeamView(View):
    def get(self,request):
        tr = True
        member = Profile.objects.filter(is_team_member=tr)

        context = {
            'member':member,
            'prf':member,
        }
        return render(request,'about/team.html',context)
    

class AboutView(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request,'about/codersource.html')
        else:
            return redirect('users:login')
