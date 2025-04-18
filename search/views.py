from django.shortcuts import render,redirect
from django.views import View
from core.models import Post
from users.models import Profile

class SearchPost(View):
    def post(self,request):
        if request.user.is_authenticated:
            q = request.POST['query']
            profile = Profile.objects.get(user=request.user)
            post = Post.objects.filter(name__icontains=q)
            context = {

                'post':post,
                'prf':profile,

            }

            return render(request,'search/post.html',context)
        else:
            return redirect('users:login')
