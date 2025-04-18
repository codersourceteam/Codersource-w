from django.shortcuts import render,redirect
from django.views import View
from users.models import *
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import math
from verification.check import check_login

banned_words = ['xxx','sex','Mason','Christian','Ateism']

class IndexView(View):
    def get(self,request):
        if request.user.is_authenticated:

            post = Post.objects.all().order_by('-no_of_likes')
            profile = Profile.objects.filter(likes__gt=5000).order_by('-likes')
            ad = Ads.objects.all()
            prf = Profile.objects.get(user=request.user)
        
           
            c = Comment.objects.all().order_by('-likes')

            context = {
                'post':post,
                'profile':profile,
                'ads':ad,
                'prf':prf,
                'tc':c,
                
            }
            ip = request.META.get('REMOTE_ADDR')
            print(ip)
            return render(request,'index.html',context)
        else:
            return redirect('users:login',)

def cmatrix(request):
    return render(request,'cmatrix/cm.html')

class ProfileView(View):
    def get(self,request,username):
        if request.user.is_authenticated:
            if User.objects.filter(username=str(username).lower()).exists():

                follower = Profile.objects.get(user=request.user)
                user1 = Profile.objects.get(user__username=username)

                if FollowersCount.objects.filter(follower=follower, user=user1).exists():
                    button_text = 'Unfollow'
                else:
                    button_text = 'Follow'

                count = ''
                flw = FollowersCount.objects.filter(user=user1).count()

            
                if flw > 1000 or flw == 1000:
                    count = 'K'
                    integer = int(flw) / 1000
                    flw = math.floor(integer)

                if flw > 1000000 or flw == 1000000:
                    count = 'M'
                    integer = int(flw) / 1000000
                    flw = math.floor(integer)
                
                if flw > 1000000000 or flw == 1000000000:
                    count = 'B'
                    integer = int(flw) / 1000000000
                    flw = math.floor(integer)


                countl = ''
                like = FollowersCount.objects.filter(follower=user1).count()

                if like > 1000 or like == 1000:
                    countl = 'K'
                    integer = int(like) / 1000
                    like = math.floor(integer)

                if like > 1000000 or like == 1000000:
                    countl = 'M'
                    integer = int(like) / 1000000
                    like = math.floor(integer)
                
                if like > 1000000000 or like == 1000000000:
                    countl = 'B'
                    integer = int(like) / 1000000000
                    like = math.floor(integer)
                
                                
                user = User.objects.get(username=str(username).lower())
                profile = Profile.objects.get(user=user)
                userprofile = Profile.objects.get(user=request.user)
                post = Post.objects.filter(user=profile)
                context = {
                    'profile':profile,
                    'prf':userprofile,
                    'usera':user,
                    'button':button_text,
                    'post':post,
                    'c':count,
                    'followers':flw,
                    'l':countl,
                    'like':like,
                }
                return render(request,'posts.html',context)
    
            else:
                return redirect ('/')
        else:
            return redirect('/')


@login_required
def like_post(request,id):
    username = request.user.username
    post_id = id

    post = Post.objects.get(id=post_id)

    like_filter = LikedPost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikedPost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect(f'/{str(post.user)}')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect(f'/{str(post.user)}')

class UploadView(View):
    def get(self,request):
        if not BanList.objects.filter(user=request.user).exists():

            profile = Profile.objects.get(user=request.user)

            context = {
                'profile':profile,
                'prf':profile,
            }
            
            return render(request,'upload.html',context)
        else:
            return redirect('core:ban')
    def post(self,request):
        user = Profile.objects.get(user=request.user)
        name = request.POST['name']
        source = request.FILES.get('source')
        caption = request.POST['caption']
        iamge = request.FILES.get('image')


        if not str(name) in banned_words or str(caption).split() in banned_words:
            if str(source).endswith('.zip') or str(source).endswith('.rar') or str(source).endswith('.rar5'):
                new_post = Post.objects.create(user=user,name=name, source=source, caption=caption,image=iamge)
                new_post.save()
                messages.info(request,'Your SourceCode uploaded!')
                return redirect('core:upload')
            else:
                messages.info(request,'Error while loading, your file must be zip,rar or rar5!')
                print(str(source).lower())
                return redirect('core:upload')
        else:
            BanList.objects.create(user=request.user)
            return redirect('core:ban')

from users.models import ViewsCount

class DetailView(View):
    def get(self,request,id):

        def createview(user,id):
            ViewsCount.objects.create(user=user,post_id=id)

        if not ViewsCount.objects.filter(user=request.user,post_id=id).first():
            createview(request.user,id)
        
        views = ViewsCount.objects.filter(post_id=id).count()
        comments = Comment.objects.filter(post=id).count()
        post = Post.objects.get(id=id)
        prf = Profile.objects.get(user__username=post.user)
        posts = Post.objects.all().order_by('-no_of_likes')
        comment = Comment.objects.filter(post=id)

        context = {
            'post':post,
            'prf':prf,
            'posts':posts,
            'views':views,
            'comments':comment,
            'cc':comments,
        }

        return render(request,'details/detail.html',context)
    


class AddQuestion(View):
    def post(self,request):
        check_login(request.user)
        question = request.POST['body']
        user = Profile.objects.get(user=request.user)
        Questions.objects.create(user=user,body=question)
        messages.info(request,"Your Question Added We'll Answer via Email Adress!")
        return redirect('/')