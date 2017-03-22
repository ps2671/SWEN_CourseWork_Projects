TOOL SHARE - APPLICATION 


TABLE OF CONTENT
* CONFIGURATION INSTRUCTIONS AND PRE-INSTALLED SOFTWARE
* INSTALLATION INSTRUCTIONS
* OPERATING INSTRUCTIONS 
* EXAMPLES
* COPYRIGHT AND LICENSING INFORMATION



CONFIGURATION INSTRUCTIONS AND PRE-INSTALLED SOFTWARE 
-----------------------------------------------------------------------------------------------------------------------------
To operate this program, one needs to have the following software pre-installed in the local machine:
* Python 3.4.3
* SQLite 2.6.0
* Django 1.9.1
* Web browser (Google Chrome, Mozilla Firefox etc.)  




INSTALLATION INSTRUCTIONS
------------------------------------------------------------------------------------------------------------------------------
To operate this program, no additional installation is needed. 
Just copy the files in the USB drive/myCourses/svn in a newly created folder, that should be named ToolShare, in the location of your choice 
in your local machine (i.e. Desktop)




OPERATING INSTRUCTIONS
----------------------------------------------------------------------------------------------------------------------------
1) Open the command prompt (search from the Start Menu).
2) Set the location to project location where manage.py is located. In the files from the USB drive/ myCourses/ svn, it is located in the main branch. 
The command to set the location in a Windows-operated machine is typing cd PathtoFolder (e.g. cd Desktop\ToolShare)
3) On that path, continue with the command "python manage.py runserver"
4) Open a web browser (i.e. Google Chrome, Mozilla Firefox, etc.)
5) Go to the localhost by typing this url "http://127.0.0.1:8000/" in your browser. 


EXAMPLES 
-----------------------------------------------------------------------------------------------------------------------------
--Registration-- 

6) 1. When a first user is registerd in a new zip-code area, this user will become the administrator and can immediately log in. 
   2. When a user registered is not the first one in a new zip-code area, s/he cannot immediately log in as s/he should be approved by the administrator. 

7)  For a user to register, s/he should: 

	a) Click the <<Don't have an account? Sign up» link. 
	b) Fill out the required information. 
	c) Click Submit. 
     The system will validate the information and will provide messages if any of the fields fail validation. The user can re-enter
	 the correctly formatted information again.

A) BASIC USER FUNCTIONALITY 

--Login & Logout-- 

8) If a user has not been approved by the admin of the ShareZone, s/he cannot login. The system assumes that the mode of notification for the
	eventual approval/dissaproval will be handled offline in the community. 
	Once a user has been approved and has been told by admin that s/he has been approved she or he can login:
		a) Provide the username in Enter Username. Provide the password in Enter Password. Click <<Login>>. 
   		b) In the horizontal navigation bar, at the far right, the user can see the logout button. Click that to log out. 

--Notifications--

9) The bell symbol in the right of the horizontal navigation on the top of the screen is the notification button. 
   Any time the user receives a notification, the bell symbol will turn blue. If the user clicks on the symbol, s/he can receive/see
	 a notification that that a tool s/he has registered is borrowed or a request has been approved by another user. 
   The notification message will inform the user about the page that is related to the notification.  		
   If there is no notification, if the user clicks on the bell, the system will say that there is no notifications for him/her at the time. 	

--Your account -- 


10) If the user clicks on the Your Acount dropdown menu, the user can see two options.
	a) Update profile - The user can change his/her information except for username and zipcode. After the user clicks <<Save>>
		 the changes are saved to the database. 
	The system will validate the information and will provide messages if any of the fields fail validation. The user can re-enter
	 the correctly formatted information again.


	b) Change your password - The user can change his/her password by :
		1. Writing in your new password in the Enter a New Password Field. 
		2. Rewriting your new password in the Confirm your New Password Field. 
		3. Pressing the <<Change Password>> button. 
	If the two fields do not match, an error will appear and you can re-enter your passwords until they match. 

--MANAGE TOOLS-- 
-- View Tools -- 

11) The user can view his/her registerd tools, edit, and activate/deactivate them. 
	a) If the user clicks the <<Edit>> button, a new window will open. 
		1. The user can change the information for the tool. 
			a) If there is no Community Shed, the only possible address for the tool will be the user's home address.
			b) If there is a Community Shed, the user can choose between his/her home or the Shed. 
		2. The user clicks <<Update>>
		3. The user is redirected to the View Tools Page. 
		
		The system will validate the information and will provide messages if any of the fields fail validation. The user can re-enter
	 	the correctly formatted information again.
		A user cannot edit the tool  if it's already being borrowed. 
	b) To deactivate the tool (the user can only do this if the tool is already activated)
		1. Click <<Activate/Deactivate>>. 
		2. The Status should turn to Unavailable.  
	The users won't be able to borrow this tool.  A user cannot deactivate the tool  if it's already being borrowed. 
	
	c) To activate the tool (the user can only do this if the tool is already deactivated)
		1. Click <<Activate/Deactivate>>. 
		2. The Status should turn to Aavailable.  
	The users will now be able to borrow this tool. 

--Add Tools--

12) The user can add new tools. 
	a) Enter the information for the tool. 
		1. If there is no Community Shed, the only possible address for the tool will be the user's home address.
		2. If there is a Community Shed, the user can choose between his/her home or the Shed. 
	b) Click <<Register the Tool>>
	c) The successful tool registration message will be displayed. 
	The system will validate the information and will provide messages if any of the fields fail validation. The user can re-enter
	 	the correctly formatted information again.
	If the user has no registered tools, the system will display the following message: "You have no registered tools."

-- Borrow Tools -- 
13) The user can borrow tools from other users in his/her sharezone. 
	a) Click the tool to be borrowed. 
	b) Specify the timeperiod. 
	The system will validate the information and will provide messages if any of the fields fail validation. The user can re-enter
	 	the correctly formatted information again.
	If there are no tools to be borrowed, the system will display the following message: "There are no available tools at this moment."

--Approve Tools -- 

14) The user can accept/reject tool requests made by other users. 
	a)To accept the request, click <<Accept>>. 
	b) To reject the request, click <<Reject>>. 
    If there are no requests for the user's tools, the system will display the following message: "No requests have been made for your tools."
    
--Return Tools -- 
15) The user can return the tools s/he has borrowed.
	a) The user clicks return.
	b) The user writes a message.
	c) The user rates the tool. 
    If the user has no tools to return, the system will display the following message: "No tools to return."	

--View Requests -- 
16) The user can see the requests s/he has made to borrow other's tools and their status. 
	If there are no requests made from the user, the system will display the following message: "No tools have been requested."

--SHAREZONE -- 
--Your ShareZone--
17)The user can see information about his/her sharezone such as the zipcode, the location of the Community Shed(if it exists) and the administrators. 

--COMMUNITY STATISTICS-- 
18)In the homepage, the user can see the statistics about his/her sharezone regarding recently added tools, the highest rated tools and information
	about his/her sharezone. 
	If there are no recently added tools or rated tools, the system will display the following messages.  	
	
	

B) ADMIN FUNCTIONALITY    	
An admin play the role of the shed coordinator. An admin can also borrow and lend tools like the basic users. As such, the basic user functionality
is also applicable to the admin users, for the most part. In the next section, only functionliaty that is specific to the admin user will be elaborated. 

--Login & Logout-- 


8) The Admin in a Sharezone, the first user within a zipcode area, can immediately log in. 
   a) Provide the username in Enter Username. Provide the password in Enter Password. Click Login. 
   b) In the horizontal navigation bar, at the far right, you can see the logout button. Click that to log out. 

-- Notifications -- 

9) The bell symbol in the right of the horizontal navigation on the top of the screen is the notification button. 
   Any time the admin receives a notification, the bell symbol will turn blue. If the user clicks on the symbol, s/he can receive/see
	 two types of notifications:
	a) Notification that a tool s/he has registered is borrowed or a request has been approved by another user. 
	b) Notification that a new user requests to join his/her sharezone. 
   The notification message will inform the user about the page that is related to the notification.  		
   If there is no notification, if the user clicks on the bell, the system will say that there is no notifications for him/her at the time. 	

--Your account -- 


10) If you click on the your account dropdown menu, you can see two options.
	a) Update profile - You can change information for the user except for username and zipcode. After you press save the changes are saved to the database. 
	The same restrictions as in the registration apply: the user cannot be less than 13 years of age, hence, the birthday cannot change to making the
	user less than 13 years. 

	b) Change your password - You can change your password by :
		1. Writing in your new password in the Enter a New Password Field. 
		2. Rewriting your new password in the Confirm your New Password Field. 
		3. Pressing the <<Change Password>> button. 
	If the two fields do not match, an error will appear and you can re-enter your passwords until they match. 


--SHAREZONE -- 
-- Your ShareZone -- 
11) With an admin account, the user can create or edit a Community Shed, which is by default set to False. 
     If no Community Shed exists, the admin user can create one. 		
	a) If the user clicks <<Create a Community Shed>> a new window will open. 
		1. Enter the address for the Community Shed. 
		2. Click <<Create Community Shed>>.
		3. Get redirected to the Your Sharezone page.
		4. See that the address of the Community Shed has changed from "No Community Shed" to the address you just provided. 
	  If the address provided in the Community Shed Creation Page contains symbols other than letters, numbers and spaces, the system will not allow you
	  to create the community shed and will provide an error message. You can re-enter the address in the correct format. 
     If the Community Shed already exists, an administrator can edit it.
		a) If the user clicks <<Edit>> a new window will open. 
		1. Enter the address for the Community Shed. 
		2. Click <<Create Community Shed>>.
		3. Get redirected to the Your Sharezone page.
		4. See that the address of the Community Shed has changed from "No Community Shed" to the address you just provided. 
	  If the address provided in the Community Shed Creation Page contains symbols other than letters, numbers and spaces, the system will not allow you
	  to edit the community shed and will provide an error message. You can re-enter the address in the correct format. 

--User Requests --   
 12) The admin approves or rejects the users that have requested to join his/her sharezone. Until all requests in this page have been approved or rejected,
	the admin will continue to receive notifications for this. 
	If there are no requests to join the sharezone, the admin will see the following message 
		"There are no requests to join your Sharezone at this moment." 	 
	If there are requests to join the sharezone, the admin can either:
		1. Click <<Approve>> and that user will join the sharezone. 
		 
		or 
		
		2. Click <<Reject>> and that user will be deleted from the database and his/her username can be used by other users. 

	As soon as the admin approves or rejects all the users, s/he will se the 
		"There are no requests to join your Sharezone at this moment." message again.  	

-- Manage Users -- 
13) The admin can edit, deactivate and reactivate, or make administrators all the users approved by him/her in his/her ShareZone. 
	a) To edit the information for a user: 
		1. Click <<Update>> (a new window will open).
		2. Update the information needed. 
		3. Click <<Save>>. 
		4. Get redirected to the Manage Users page. 
	If any of the fields fail validation, the system will display a proper error. You can re-enter the information in the correct format. 

	b) To deactivate the user: (the admin can only do this if the user is already activated)
		1. Click <<Deactivate>>. 
		2. The button's value should turn to Activate. 
	The user won't be able to log-in if s/he has been deactivated. 
	
	c) To activate the user: (the admin can only do this if the user is already deactivated)
		1. Click <<Activate>>. 
		2. The button's value should turn to <<Deactivate>>. 
	The user will now be able to login. 
	d) To make a user administrator: (the admin can only do this if the user is not an administrator).
		1. Click <<Make Admin>>
		2. The button should change to text that says 'Is Admin' 
	The ShareZone Admin cannot change the status of other Admins to Basic Users. Only a system administrator can do that. 

-- Manage Tools -- 
14) The admin can edit, deactivate and reactivate all the tools registered by users approved by him/her in his/her ShareZone. 
	a) To edit the information for a tool. 
		1. Click <<Update>> (a new window will open).
		2. Update the information needed. 
		3. Click <<Save>>. 
		4. Get redirected to the Manage Tools page. 
	If any of the fields fail validation, the system will display a proper error. You can re-enter the information in the correct format. 
	 An admin can edit the tool even if it's already being borrowed. 

	b) To deactivate the tool (the admin can only do this if the tool is already activated)
		1. Click <<Activate/Deactivate>>. 
		2. The Status should turn to Unavailable.  
	The users won't be able to borrow this tool.  An admin can deactivate the tool even if it's already being borrowed. 
	
	c) To activate the tool (the admin can only do this if the tool is already deactivated)
		1. Click <<Activate/Deactivate>>. 
		2. The Status should turn to Aavailable.  
	The users will now be able to borrow this tool.


--SYSTEM ADMINISTRATOR--

The system administrator is not a basic user, nor an admin user in the ToolShare system. The system administrator can log-in and log-out like other users,
	but s/he cannot borrow, lend or register tools. The section below elaborates the functionalities that the system administrator can perform. 
	The accounts for system administrators need to be created by the Django Valoeris team. 

To access the system administrator page, go to the main page, enter the following credentials:
	username: system_admin 
	password: ToolShare2017
	Click <<Log in>>. 	

The System Admin can see statistics about the Toolshare overall, such as the number of the users, sharezones and tools. 

--User Management-- 
The system admin can view, update, deactivate and change the status of all users in all the sharezones. 
	a) To edit the information for a user: 
		1. Click <<Update>> (a new window will open).
		2. Update the information needed. 
		3. Click <<Save>>. 
		4. Get redirected to the Manage Users page. 
	If any of the fields fail validation, the system will display a proper error. You can re-enter the information in the correct format. 

	b) To deactivate the user: (the admin can only do this if the user is already activated)
		1. Click <<Deactivate>>. 
		2. The button's value should turn to Activate. 
	The user won't be able to log-in if s/he has been deactivated. 
	
	c) To activate the user: (the admin can only do this if the user is already deactivated)
		1. Click <<Activate>>. 
		2. The button's value should turn to <<Deactivate>>. 
	The user will now be able to login. 
	d) To make a user administrator: (the admin can only do this if the user is not an administrator).
		1. Click <<Make Admin>>
		2. The button should change to text that says 'Make Basic User'. 
	e) To make a user a basic user: (the admin can only do this if the user is an administrator).
		1. Click <<Make Basic User>>
		2. The button should change to text that says 'Make Admin'. 

--Sharezone Management -- 
The system admin can view and create/edit the shed for any sharezone.
	  If no Community Shed exists, the system admin user can create one. 		
	a) If the user clicks <<Edit>> a new window will open. 
		1. Enter the address for the Community Shed. 
		2. Click <<Create Community Shed>>.
		3. Get redirected to the Manage Sharezones page.
		4. See that the address of the Community Shed has changed from "No Community Shed" to the address you just provided. 
	  If the address provided in the Community Shed Creation Page contains symbols other than letters, numbers and spaces, the system will not allow you
	  to create the community shed and will provide an error message. You can re-enter the address in the correct format. 
     If the Community Shed already exists, a system administrator can edit it.
		a) If the user clicks <<Edit>> a new window will open. 
		1. Enter the address for the Community Shed. 
		2. Click <<Create Community Shed>>.
		3. Get redirected to the Your Sharezone page.
		4. See that the address of the Community Shed has changed from "No Community Shed" to the address you just provided. 


-- Tool Management -- 

 The system admin can edit, deactivate and reactivate all the tools registered by users. 
	a) To edit the information for a tool. 
		1. Click <<Update>> (a new window will open).
		2. Update the information needed. 
		3. Click <<Save>>. 
		4. Get redirected to the Manage Tools page. 
	If any of the fields fail validation, the system will display a proper error. You can re-enter the information in the correct format. 
	 An admin can edit the tool even if it's already being borrowed. 

	b) To deactivate the tool (the admin can only do this if the tool is already activated)
		1. Click <<Activate/Deactivate>>. 
		2. The Status should turn to Unavailable.  
	The users won't be able to borrow this tool.  An admin can deactivate the tool even if it's already being borrowed. 
	
	c) To activate the tool (the admin can only do this if the tool is already deactivated)
		1. Click <<Activate/Deactivate>>. 
		2. The Status should turn to Aavailable.  
	The users will now be able to borrow this tool.
	 




COPYRIGHT AND LICENSING INFORMATION
------------------------------------------------------------------------------------------------------------------------------
1) This web-application was developed by Valar Djangoeris Team, as part of SWEN-610 Class in RIT. 


