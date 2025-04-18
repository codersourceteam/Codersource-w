from django.shortcuts import render,redirect
from django.views import View
from .check import check_staff
from verification.models import VerReq
from core.models import Post,Profile,Questions
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from verification.check import check_login
from django.contrib import messages



class IndexView(View):
    def get(self,request):
        check_login(request.user)
        if check_staff(request.user):

            vers = VerReq.objects.all()
            posts = Post.objects.all()
            questions = Questions.objects.all().order_by('is_seen')
            count = posts.count()
            countver = vers.count()
            profile = Profile.objects.get(user=request.user)
            context = {
                'vers':vers,
                'posts':posts,
                'count':count,
                'vercount':countver,
                'prf':profile,
                'questions':questions,

            }

            return render(request,'modder/index.html',context)
        else:
            return redirect('core:index')
        
class EditVer(View):
    def get(self,request,id):
        check_login(request.user)
        if check_staff(request.user):
            ver = VerReq.objects.get(uid=id)
            profile = Profile.objects.get(user=request.user)
            context = {

                'ver':ver,
                'prf':profile
            }
            return render(request,'modder/ver.html',context)

        else:
            return redirect('/')


class Verify(View):
    def get(self,request,id):
        check_login(request.user)
        if check_staff(request.user):
            req = VerReq.objects.get(uid=id)
            usr = Profile.objects.get(user__username=req.user)
            email = req.email
            usr.is_verified = True
            req.delete()
            usr.save()
            now = datetime.now()

            try:
                subject = 'Coder | Source'
                message = f"""
                
                Your Verification Request Applied
                at {now} by {request.user.username} 
                
                Thanks For Using!

                """ 
                send_mail(subject, 
                message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

                return redirect('moderator:index')
            except:
                return redirect('moderator:index')
        else:
            return redirect('/')
        

class EditPost(View):
    def get(self,request,post):
        check_login(request.user)
        if check_staff(request.user):

            p = Post.objects.get(id=post)
            context = {

                'post':p

            }

            return render(request,'modder/post.html',context)
        
        else:
            return redirect('/')
        
    def post(self,request,post):
        check_login(request.user)
        if check_staff(request.user):
            name = request.POST['name']
            caption = request.POST['caption']
            image = request.FILES.get('image')
            source = request.FILES.get('source')

            if request.FILES.get('image') != None or request.FILES.get('source') != None:
                p = Post.objects.get(id=post)
                p.image = image
                p.source = source
                p.name = name
                p.caption = caption
                p.save()
                return redirect('moderator:index')
            else:
                p = Post.objects.get(id=post)
                p.name = name
                p.caption = caption
                p.save()
                return redirect('moderator:index')
        else:
            return redirect('/')

class DeletePost(View):
    def get(self,request,post):
        check_login(request.user)
        if check_staff(request.user):

            req = Post.objects.get(id=post)
            req.delete()
            messages.info(request,'Success!!')
            return redirect('moderator:index')
           
        else:
            return redirect('/')
        

from django.contrib.auth.models import User

class Answer(View):
    def get(self,request,id):
        q = Questions.objects.get(uid=id)
        q.is_seen = True
        q.save()
        context = {
            'question':q
        }
        return render(request,'modder/answer.html',context)
    def post(self,request,id):
        q = Questions.objects.get(uid=id)
        answer = request.POST['answer']
        email = User.objects.get(username=q.user.user.get_username())
        print(email.email)

        q.delete()

        try:
            subject = 'Coder | Source'
            message = f"""
            You've requested a question

            Question : {q.body}

            Answer : {answer}
            
            Thanks For Using!

            """ 
            send_mail(subject, 
            message, settings.EMAIL_HOST_USER, [email.email], fail_silently=False)
            

            return redirect('moderator:index')
        except:
            return redirect('moderator:index')



