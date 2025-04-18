from django.shortcuts import render,redirect
from django.views import View
from core.models import Post
from django.contrib import messages

class EditPostView(View):
    def get(self,request,id):
        post = Post.objects.get(id=id)
        if post.user.user != request.user:
            return redirect('/')
        else:
            context = {
                'post':post,
            }
            return render(request,'details/edit_post.html',context)
    def post(self,request,id):
        name = request.POST['name']
        image = request.FILES.get('image')
        caption = request.POST['caption']
        file = request.FILES.get('file')

        new_post = Post.objects.get(id=id)
        new_post.name = name
        new_post.image = image
        new_post.caption = caption
        new_post.file = file
        new_post.save()
        messages.info(request,'Changed Successfully!')
        return redirect(f'/edit/post/{id}')
        
