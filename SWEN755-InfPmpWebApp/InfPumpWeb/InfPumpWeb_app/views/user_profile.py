from django.shortcuts import render
from django.http import HttpResponseRedirect
from InfPumpWeb_app.views.session import __is_session_open
from InfPumpWeb_app.views.user_details import __add_general_content_to_context
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from InfPumpWeb_app.models import *
from django.contrib.auth.models import User

@login_required(login_url='/accounts/login/')
def user_profile(request):
    if not __is_session_open(request):
        return HttpResponseRedirect('/')
        
    curr_user = User.objects.get(username=request.user)
    userProfile = UserProfile.objects.get(user=curr_user)

  

    context = {
        'user_type': userProfile.type,
    }

    context.update(__add_general_content_to_context(curr_user,userProfile))

    return render(request, 'user_profile.html', context)

# end profile
