from django.shortcuts import render
from django.http import HttpResponseRedirect
from InfPumpWeb_app.views.user_details import __add_general_content_to_context
from InfPumpWeb_app.views.session import __is_session_open
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from InfPumpWeb_app.models import *
from django.contrib.auth.models import User

@login_required(login_url='/accounts/login/')
def list(request):
    if not __is_session_open(request):
        return HttpResponseRedirect('/')

    user = User.objects.get(username=request.session['user_username'])
    userProfile = UserProfile.objects.get(user=user)

    patient_list = UserProfile.objects.all().filter(type='Patient')
    for p in patient_list:
        print(p.user.first_name)
    context = {
        'user_type': userProfile.type,
        'list_page': True,
        'patient_list':patient_list
    }

    context.update(__add_general_content_to_context(user,userProfile))

    return render(request, 'list.html', context)

