CONFIGURATION INSTRUCTIONS
----------------------------
----------------------------
Please install the following software in your system -

1) Python 3.4.3 (https://www.python.org/downloads/release/python-343/)

2) SQLite 2.6.0 

3) Django 1.9.1 (https://pypi.python.org/pypi/Django/1.9.1) (https://www.djangoproject.com/download/)


OPERATING INSTRUCTIONS
----------------------------
----------------------------
1) Open the command prompt (from start menu).
2) Set the location to project location where "manage.py" file is located. The command to set the location
	in a Windows-operated machine is cd PathSpecified (e.g. cd Desktop\Assignment 3\InfPumpWeb)
3) Continue with the command "python manage.py runserver"
4) Open a web browser(i.e. Google Chrome, Mozilla Firefox, etc.)
5) Go to the localhost through this url "http://127.0.0.1:8000/"



EXAMPLES 
----------------------------
----------------------------
Open 3 browser google chrome tabs. One in normal mode and other two tabs in Incognito (Ctrl + Shift + N) mode.
----------------------------

** 1st User Credentials :

Username : Admin
Password : 123456

For Admin	: 		"View All Patients" & "Doctor List" options will display on home page.
----------------------------
** 2nd User Credentials :

Username : patient1
Password : 123456

For Patient :		"View All Doctors" option will display on home page.
----------------------------
** 3rd User Credentials :

Username : doctor1
Password : 123456

For Doctor  : 		"View All Patients" & "Prescription" options will display on home page.


SESSION MANAGMENT
----------------------------
----------------------------

1) If any user is inactive for 60 seconds, the user session will expire and the user is forced to login again and redirected to login page.

2) If the user closes the browser, the user is logged out of the application and the user session is ended.

3) The user session details like session key, session data and expire_date are stored in the database table "django_session".

4) If the user tries to access any page of the application without logging in to the application, the user is redirected to the login page.

----------------------------
----------------------------