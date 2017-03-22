from django.http import HttpResponseRedirect
from InfPumpWeb_app import models
from InfPumpWeb_app.forms import login_form
from InfPumpWeb_app.views.session import __login_open_session
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def user_login(request):

    form = login_form.UserLogger(request.POST or None)

    context = {
        'login_form': form,
        'login_page': True,

    }

    if form.is_valid():
        # verify if user with the entered username and password exists
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(request, user)
            return __login_open_session(request, form.cleaned_data['username'])
        else:
            # if not, store the error message in the context
            error = 'Invalid username or password. Please try again.'
            context['error'] = error

    return render(request, 'home.html', context)


# end user_login


# end __is_session_open