from django.shortcuts import render,redirect
from django.views import View
from users.models import Profile
from .models import *
from verification.check import check_login
from django.contrib import messages

class DirectView(View):
    def get(self,request,username):
        check_login(request.user)
        user = Profile.objects.get(user__username=username)
        usr = Profile.objects.get(user=request.user)
        
        if Inbox.objects.filter(owner=user).exists():
            messages = Inbox.objects.filter(owner=user)
        elif Inbox.objects.filter(user=user).exists():
            messages = Inbox.objects.filter(user=user)
        else:
            messages = None
        

        context = {
            'messages':messages,
            'profile':user,
            'prf':user,
            'usr':usr,

        }

        return render(request, 'direct/message.html', context)
    

class InboxView(View):
    def get(self,request,id):
        check_login(request.user)

        inbox = Message.objects.filter(inbox__uid=id)
        profile = Profile.objects.get(user=request.user)
        try:
            message = Inbox.objects.get(uid=id)
        except:
            print('Inbox Not Found')

        rp = Profile.objects.get(user=request.user)

        inb = Message.objects.filter(inbox__uid=id,receiver=rp)
        inb.update(is_read=True)
        
        msg = UnreadMessage.objects.filter(message__uid=id)
        msg.delete()

        try: 
            if Inbox.objects.get(user=rp,uid=id):
                receiver = Inbox.objects.get(uid=id).owner
        except:
            if Inbox.objects.get(owner=rp,uid=id):
                receiver = Inbox.objects.get(uid=id).user
            
        context = {
            'message':message,
            'inbox':inbox,
            'prf':profile,
            'receiver':receiver,

        }

        return render(request,'direct/inbox.html',context)
    
    # def post(self,request,username):
    #     return redi

class SendMessage(View):
    def post(self,request,id,sender,receiver):
        check_login(request.user)
        prf = Profile.objects.get(user=request.user)
        message = request.POST['message']
        if Inbox.objects.filter(user=prf).exists() or Inbox.objects.filter(owner=prf).exists():
            mes = Inbox.objects.get(uid=id)
            s = Profile.objects.get(user__username=sender)
            r = Profile.objects.get(user__username=receiver)
            new = Message.objects.create(inbox=mes,sender=s,receiver=r,message=message)
            UnreadMessage.objects.create(message=new)
            return redirect(f'/direct/inbox/{id}')
        else:
            messages.info(request,'Do Not Mess!')
            return redirect('users:logout')

class CreateChatView(View):
    def get(self,request,receiver):
        check_login(request.user)
        profile = Profile.objects.get(user=request.user)
        receiver_profile = Profile.objects.get(user__username=receiver)
        if Inbox.objects.filter(user=receiver_profile,owner=profile).exists() or Inbox.objects.filter(user=profile,owner=receiver_profile).exists():
            try:
                inb = Inbox.objects.get(user=receiver_profile,owner=profile)
            except:
                inb = Inbox.objects.get(user=profile,owner=receiver_profile)
            return redirect(f'/direct/inbox/{inb.uid}')
        else:
            context = {
                    'prof':receiver_profile
                }
            return render(request,'direct/new_inbox.html',context)
        
    def post(self,request,receiver):
        receiver_pr = Profile.objects.get(user__username=receiver)
        owner = Profile.objects.get(user=request.user)
        message = request.POST['message']
        new = Inbox.objects.create(owner=owner,user=receiver_pr)
        new_m = Message.objects.create(inbox=new,message=message,sender=owner,receiver=receiver_pr)
        return redirect(f'/direct/inbox/{new.uid}')

