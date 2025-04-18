from django.shortcuts import redirect,render
def check_login(user):
    if user.is_authenticated:
        pass
    else:
        return redirect('/')