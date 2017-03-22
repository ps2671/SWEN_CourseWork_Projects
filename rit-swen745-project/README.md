# rit-swen745-project
A web-based paper submission and review system for a workshop named "Software Architecture Mining"


NOTES
----------------------------
This project uses the GitHub project "django-notifications" in a modified form suitable to our needs. Please see the LICENSE.txt file for copyright information for the "django-notifications" project.


CONFIGURATION INSTRUCTIONS
----------------------------
Please install the following software in your system:

1) Python 3.4.3
2) SQLite 2.6.0
3) Django 1.9.1


OPERATING INSTRUCTIONS
----------------------------
1) Open the command prompt (from start menu).
2) Set the location to project location where manage.py is located. The command to set the location in a Windows-operated machine is cd PathSpecified (note: use quotes around your path if the path contains spaces, e.g. cd "Desktop\Demo Project")
3) On that path, type the command "python manage.py makemigrations" and press enter 
4) Continue with typing the command "python manage.py migrate" and press enter
5) Continue with the command "python manage.py runserver"
6) Open a web browser(i.e. Google Chrome, Mozilla Firefox, etc.)
7) Go to the localhost through this url "http://localhost:8000/"


EXAMPLES 
----------------------------
--Login-- 
8)Use "user_sam" for the username and "123" for the password. 

--Logout-- 
9)Click the logout button.  

--My Profile -- 
10)Click My Profile to see the saved data on "user_sam".

--Make Submission -- 
11) Click on "Make Submission" to submit a document.

--Registration -- 
12) Click on "Registration" and fill in the required fields to register an user.

--Create Super User -- 
13.1) Open the command prompt (from start menu).
13.2) Set the location to project location where manage.py is located. The command to set the location in a Windows-operated machine is cd PathSpecified (note: use quotes around your path if the path contains spaces, e.g. cd "Desktop\Demo Project")
13.3) python manage.py createsuperuser
