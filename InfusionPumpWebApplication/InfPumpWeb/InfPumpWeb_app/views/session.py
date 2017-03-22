from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required(login_url='/accounts/login/')
def __login_open_session(request, username):

	curr_user = User.objects.get(username=request.user)

    # open the session
	request.session['is_open']=True
    # set the universal user email
	request.session['user_email']=curr_user.email
     # set the universal user username
	request.session['user_username']=username

	#Expire time is set to 60 seconds.
	request.session.set_expiry(60)

	# if request.session:
	# 	return HttpResponseRedirect('/user_profile')
	# else:
	# 	error1 = 'Session Expired due to inactiviy. Please Login Again'
	# 	context['error1'] = error1
	# 	return render(request, 'home.html', context)

	return HttpResponseRedirect('/user_profile')
# end __login_open_session

def __is_session_open(request):
    # verify if a session has been open or not
    return request.session['is_open']