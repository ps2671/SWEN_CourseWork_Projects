from InfPumpWeb_app.models import user_model
from InfPumpWeb_app.forms import registration_form
from InfPumpWeb_app.views.session import __login_open_session
from django.shortcuts import render
from django.contrib.auth.models import User
from InfPumpWeb_app.models import *

def user_registration(request):
    form_personal_info = registration_form.UserRegistrar(request.POST or None)

    context = {
        'form_user_personal_information': form_personal_info,
        'registration_page': True
    }

    if form_personal_info.is_valid():

        user = User.objects.create_user(
                username=form_personal_info.cleaned_data['username'],
                password=form_personal_info.cleaned_data['password'],
                #password2=form.cleaned_data['password2'],
                email=form_personal_info.cleaned_data['email'],
                first_name=form_personal_info.cleaned_data['first_name'],
                last_name=form_personal_info.cleaned_data['last_name']
            )

        userProfile=UserProfile(user=user)

        user.save()
        userProfile.save()

        return __login_open_session(request, user.email)

    return render(request, 'registration.html', context)

# end user_registration
