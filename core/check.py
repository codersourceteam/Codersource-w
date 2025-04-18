from django.shortcuts import redirect

def check_ip(request,url):
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip is not None:
        return redirect(url)
    else:
        return 