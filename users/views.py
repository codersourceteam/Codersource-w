from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from django.contrib import messages
from django.conf import settings
import uuid
from django.core.mail import send_mail
import random
from .models import *
from core.models import BanList
import math
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import check_password


class LogInView(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request,'login.html')
    def post(self,request):
        username = str(request.POST['username']).lower()
        password = str(request.POST['password']).lower()
        if not BanList.objects.filter(user=username).exists():
            
            prf = Profile.objects.get(user__username=username)
            if prf.is_activated:
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    return redirect('/')
                else:
                    messages.info(request, 'Login Information Invalid')
                    return redirect('users:login')
            else:
                aid = Request.objects.get(user=prf.user.get_username())
                return redirect(f'/auth/verify/{aid.id}')

            
        else:
            messages.info(request, 'This account was banned!')
            return redirect('users:login')


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('users:login')  



            
class SignUpView(View):

    def create_verification_code(self):
            return "".join(random.sample([str(num) for num in range(0,10) ], 6 ))

    def get(self,request):
        if request.user.is_authenticated:
            return redirect('core:index')
        else:
            return render(request,'signup.html')
    def post(self,request):
        username = request.POST['username']
        email = str(request.POST['email']).lower()
        password = str(request.POST['pass']).lower()
        password2 = str(request.POST['conf']).lower()
        name = request.POST['name']


        if not BanList.objects.filter(user=username).exists() :
            if password == password2:
        
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Taken')
                    return redirect('users:signup')
                elif User.objects.filter(username=str(username).lower()).exists():
                    messages.info(request, 'Username Taken')
                    return redirect('users:signup')
                elif not str(username).isalnum():
                    messages.info(request, 'username must contain only letter and numbers')
                    return redirect('users:signup')
                else:
                    user = User.objects.create_user(username=str(username).lower(), email=email, password=password,first_name=name)
                    user.save()


                    user_model = User.objects.get(username=str(username).lower())
                    new_profile = Profile.objects.create(user=user_model, id_user=user_model.id, name=name)
                    new_profile.save()
                    id = uuid.uuid4()
                    verification_code = self.create_verification_code()

                    subject = 'Welcome to Coder | Source'
                    message = f"""
                    
                    You have registred your gmail adress please verify it
                    verification code is : {verification_code}
                    do not give this code somebody else

                    """ 
                    try:
                        send_mail(subject, 
                        message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
                        messages.info(request,'Email successfully sent!')
                    
                        Request.objects.create(code=verification_code,email=email,id=id,user=str(username).lower())
                    except:
                        messages.info(request,'Having Trouble with connection!')
                        Request.objects.create(code=verification_code,email=email,id=id,user=str(username).lower())

                    

                    print()
                    print()
                    print()
                    print()
                    print(verification_code)
                    print()
                    print()
                    print()
                    print()
                    print()


                    return redirect(f'/auth/verify/{id}')

            else:
                messages.info(request, 'Password Not Matching')
                return redirect('users:signup')
        else:
            return redirect('core:ban')


class ForgotView(View):


    def create_verification_code(self):
        return "".join(random.sample([str(num) for num in range(0,10) ], 6 ))


    def get(self,request):
        if request.user.is_authenticated:
            return redirect ('/')
        else:

            return render(request, 'auth/forgot.html')


    def post(self,request):
        if request.user.is_authenticated:
            return redirect ('/')
            
        else:
            id = uuid.uuid4()
            email = request.POST['email']
            if User.objects.filter(email=email).exists():
                try:
                    verification_code = self.create_verification_code()
                    subject = 'Coder | Source'
                    message = f"""
                    
                    You have requested to reset your password
                    verification code is : {verification_code} 
                    do not give this code somebody else

                    """ 
                    send_mail(subject, 
                    message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

                    messages.info(request,'Email successfully sent!')
                    print()
                    print()
                    print()
                    print()
                    print()
                    print(verification_code)
                    print()
                    print()
                    print()
                    print()
                    print()
                    print()
                    print()
                    Request.objects.create(code=verification_code,email=email,id=id)
                    return redirect(f'/auth/changepass/{id}')
                except:
                    messages.info(request,'Having trouble with connection or etc!')
                    print(verification_code)
                    Request.objects.create(code=verification_code,email=email,id=id)
                    return redirect('users:forgot')
            else:
                messages.info(request,'This email adress is not registered to our platform check out your email!')
                return redirect('users:forgot')



class ChangeView(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            return redirect('users:logout')
        else:
            if Request.objects.filter(id=id).exists:
                return render(request,'auth/verification.html')
            else:
                return redirect('/')

    def post(self,request,id):
        code = request.POST['ver']

        if Request.objects.filter(code=code):
            return redirect('/')
        else:
            messages.info(request,'Verification code Invalid')
            return redirect(f'/auth/changepass/{id}')


class VerifyView(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            return redirect('users:logout')
        else:
            if Request.objects.filter(id=id).exists():
                return render(request,'verify.html')
            else:
                return redirect('/')

    def post(self,request,id):
        code = request.POST['ver']

        if Request.objects.filter(code=code).exists():
            usr = Request.objects.get(id=id)
            usera = User.objects.get(username=usr.user)
            p = Profile.objects.get(user=usera)
            p.is_activated = True
            p.save()
            print(p.id_user)
            usr.delete()
            
            messages.info(request,'Activated ✅ Log Into your account')
            return redirect('users:login')
        else:
            messages.info(request,'Verification code Invalid')
            return redirect(f'/auth/verify/{id}')


class SettingsView(View):
    def get(self,request):
        if request.user.is_authenticated:
            if Profile.objects.filter(user=request.user).exists():
                user_profile = Profile.objects.get(user=request.user)
                usr = User.objects.get(username=request.user.username)
                print(usr.password)
                return render(request, 'settings.html', {'user_profile': user_profile})
            else:
                return redirect('users:logout')
        else:
            return redirect('users:login')
    def post(self,request):
        if Profile.objects.filter(user=request.user).exists():
            user_profile = Profile.objects.get(user=request.user)
            usr = User.objects.get(username=request.user.username)
            if request.FILES.get('image') == None:
                
                if len(request.POST['name']) > 15 or len(request.POST['name']) == 0:
                    messages.info(request, 'Name must contain 15 letters no more than or less than 0!')
                    return redirect('users:settings')
                else:
                    image = user_profile.profileimg
                    bio = request.POST['bio']
                    name = request.POST['name']
                    username = request.POST['username']
                    user_profile.profileimg = image
                    user_profile.bio = bio
                    user_profile.name = name
                    usr.username = username
                    
                    usr.save()
                    user_profile.save()
                    messages.info(request, 'Changes saved now LogInto your account! ')
                    return redirect('users:logout')

            
            if request.FILES.get('image') != None:
                if str(request.FILES.get('image')).endswith('.png') or str(request.FILES.get('image')).endswith('.jpg'):
                    if len(request.POST['name']) > 15 or len(request.POST['name']) < 0:
                        messages.info(request, 'Name must contain 15 letters no more than or less than 0!')
                        return redirect('users:settings')
                    else:
                        image = request.FILES.get('image')
                        bio = request.POST['bio']
                        name = request.POST['name']
                        username = request.POST['username']
                        user_profile.profileimg = image
                        user_profile.bio = bio
                        usr.username = username
                        user_profile.name = name
                        usr.save()
                        user_profile.save()
                        messages.info(request, 'Changes saved now LogInto your account! ')
                        return redirect('users:logout')
                else:
                    messages.info(request, 'Your profile picture must be png or jpg!')
                    return redirect('users:settings')

        else:
            return redirect('users:logout')


class FollowView(View):
    def get(self,request,usr):
        follower = Profile.objects.get(user=request.user)
        user = Profile.objects.get(user__username=usr)

        if FollowersCount.objects.filter(follower=follower, user=user).exists():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect(f'/{user}/')
        else:
            if not follower == user:
                new_follower = FollowersCount.objects.create(follower=follower, user=user)
                new_follower.save()
                return redirect(f'/{usr}/')
            else:
                messages.info(request,"Don't follow yourself !!")
                return redirect('users:logout')
        


class FollowersView(View):
    def get(self,request,username):
        
        if request.user.is_authenticated:
            follower = Profile.objects.get(user=request.user)
            usr = Profile.objects.get(user__username=username)

            if FollowersCount.objects.filter(follower=follower, user=usr).first():
                button_text = 'Unfollow'
            else:
                button_text = 'Follow'

            count = ''
            flw = FollowersCount.objects.filter(user=usr).count()

        
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
            like = FollowersCount.objects.filter(follower=usr).count()

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


            prf = Profile.objects.get(user__username=username)


            if FollowersCount.objects.filter(user=usr).exists():
                pr = FollowersCount.objects.filter(user=usr)
                pr1 = FollowersCount.objects.filter(follower=usr)
                context = {
                    'prf':prf,
                    'profile':prf,
                    'pr':pr,
                    'button':button_text,
                    'c':count,
                    'followers':flw,
                    'l':countl,
                    'like':like,
                    'pr1':pr1,
                }
                return render(request,'followers.html',context)

            else:
                return redirect(f'/{username}/')
        else:
            messages.info(request,'Log In First')
            return redirect('users:login')
    


class AllUsers(View):
    def get(self,request):
        users = Profile.objects.all()
        count =users.count()
        prf = Profile.objects.get(user=request.user)

        for u in users:
            print()
            print()
            print()
            print()
            print()
            print()
            print(u.user.get_username())
            print(u.uid)



        context = {
            'users':users,
            'c':count,
            'prf':prf
        }
        return render(request,'all/all.html',context)


def AddComment(request,id):
    if request.user.is_authenticated:
        comment = request.POST['comment']
        if not len(comment) == 0:
            prof = Profile.objects.get(user=request.user)
            Comment.objects.create(user=prof,post=id,comment=comment)
            return redirect(f'/detail/{id}')

        else:
            return redirect(f'/detail/{id}')
    else:
        return redirect('users:login')
    
class ChangePassword(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'auth/changepassword.html')

    @method_decorator(login_required)
    def post(self, request):
        old_password = request.POST['old']
        new_password = request.POST['new']
        confirm_password = request.POST['confirm']

        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('users:changepas')

        user = request.user
        if not check_password(old_password, user.password):
            messages.error(request, 'Old password is incorrect.')
            return redirect('users:changepas')

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  # Important to keep the user logged in after password change
        messages.success(request, 'Your password was successfully updated! Login Again')
        return redirect('users:logout')