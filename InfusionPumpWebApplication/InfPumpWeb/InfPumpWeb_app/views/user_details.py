import datetime

# private function dedicated to the addition of common fields in context
# private function dedicated to the addition of common fields in context
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from InfPumpWeb_app.models import *


def __add_general_content_to_context(curr_user,userProfile):
	
	context = {
        'user_first_name': curr_user.first_name,
        'user_type': userProfile.type,
        'date': datetime.datetime.now(),
    }

	return context