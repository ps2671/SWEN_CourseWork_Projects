from django.http import HttpResponseRedirect
from django.contrib.auth import logout

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')