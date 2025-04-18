from django.shortcuts import render,redirect
from users.models import Comment,Profile
from core.models import Post

def DeleteComment(request,id,post):
    if request.method == 'GET':
        if request.user.is_authenticated:
            comment = Comment.objects.get(uid=id)
            profile = Profile.objects.get(user=request.user)
            if comment.user == profile:
                comment.delete()
            else:
                return redirect('users:logoout')
            return redirect(f'/detail/{post}')
        else:
            return redirect('users:login')
    else:
        return redirect('/')
    
def DeletePost(request,id):
    if request.method == 'GET':
        if request.user.is_authenticated:
            post = Post.objects.get(id=id)
            prof = Profile.objects.get(user=request.user)
            if post.user == prof:
                post.delete()
                return redirect('/')
            else:
                return redirect('users:logout')
        else:
            return redirect('users:login')
    else:
        return redirect('users:logout')