from InfPumpWeb_app.forms import update_user_info_form
from django.shortcuts import render
from django.http import HttpResponseRedirect
from InfPumpWeb_app.views.session import __is_session_open
from InfPumpWeb_app.views.user_details import __add_general_content_to_context
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from InfPumpWeb_app.models import *
from django.contrib.auth.models import User

# User Manage Account
@login_required(login_url='/accounts/login/')
def manage_account(request):
    if not __is_session_open(request):
        return HttpResponseRedirect('/')
        
    user = User.objects.get(username=request.session['user_username'])
    userProfile = UserProfile.objects.get(user=user)


    # put all the initial for fields in this dict
    initial_form_data = {'first_name': user.first_name,
                         'last_name': user.last_name,
                         'email': user.email,
                         'manage_account_page' : True
                         }

    if request.method == 'GET':
        form_personal_info = update_user_info_form.ManageAccount(initial_form_data)

        context = {
            'form_user_personal_information': form_personal_info,
        }

        context.update(__add_general_content_to_context(user,userProfile))

    if request.method == 'POST':
        form_personal_info = update_user_info_form.ManageAccount(request.POST or None)

        context = {
            'form_user_personal_information': form_personal_info,
        }

        context.update(__add_general_content_to_context(user,userProfile))

        if form_personal_info.is_valid():

            user.first_name = form_personal_info.cleaned_data['first_name']
            user.last_name = form_personal_info.cleaned_data['last_name']
            user.email = form_personal_info.cleaned_data['email']
            # store the user in the db
            user.save()
            messages.success(request, 'You have successfully updated your information')
            return HttpResponseRedirect('/user_profile')

    return render(request, 'manage_account.html', context)

    # End manage account
