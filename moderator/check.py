from django.shortcuts import redirect

def check_staff(user):
    if user.is_staff:
        return True
    else:
        return False