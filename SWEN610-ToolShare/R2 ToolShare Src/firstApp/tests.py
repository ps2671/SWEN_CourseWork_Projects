"""
Writing unit tests for forms, models and views.
Run by using this command - "manage.py test".

"""
from django.test import TestCase,Client
from firstApp.forms import *
from firstApp.models import *
from django.contrib.auth.models import User
from datetime import date
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
# Create your Model tests here.
class modelTests(TestCase):

	# Initial Setup for testing the models.
	def setUp(self):
		self.testUser = User.objects.create_user('test_user1','test_user1@toolshare.com','123')
		self.testUserProfile = UserProfile.objects.create(user=self.testUser,
			first_Name='test user1 fn',last_Name='test user1 ln',address='123 Street st.',zipCode='12345',
			pickupArrangements='car',date='2015-10-10')
		self.toolRegister = ToolsRegister.objects.create(userProfile=self.testUserProfile,
                                         nameOfTheTool='test_hammer',
                                         addressOfTheTool='Rustic Village',
                                         statusOfTheTool='Available',
                                         categoryOfTheTool='Hammer',
                                         conditionOfTheTool='Good',
                                         toolDescription='Its a nice hammer'
                                         )

		self.toolRequest = ToolRequest.objects.create(toolId = self.toolRegister,
    												requester_id = '1',
    												requestedFromDate = date.today(),
    												requestedToDate = date.today(),
    												requestStatus = '1'
    												)

		self.toolBorrowed = ToolBorrowed.objects.create(toolId = self.toolRegister,
    													requestId = self.toolRequest,
    													borrowerId = '2',
    													notified = 1
    													)

		self.toolRejected = ToolRejected.objects.create(toolId = self.toolRegister,
    													requestId = self.toolRequest,
    													requesterId = '1',
    													rejectionReason = 'Rejected',
    													notified = 1
    													)

		self.toolReturn = ToolReturn.objects.create(toolId = self.toolRegister,
    												requestId = self.toolRequest,
    												note = 'Thank You',
    												rating = '1'
    												)
	# Initial Setup for testing the User and UserProfile Model.
	def test_user_model(self):
		self.testUser1 = User.objects.create_user('test_user11','test_user11@toolshare.com','123')
		self.testUserProfile = UserProfile.objects.create(user=self.testUser1,
			first_Name='test user1 fn',last_Name='test user1 ln',address='123 Street st.',zipCode='12345',
			pickupArrangements='car',date='2015-10-10')
		usr = User.objects.get(username="test_user11")
		self.assertEqual(usr.email,'test_user11@toolshare.com')
		usr_prf = UserProfile.objects.get(id=1)
		self.assertTrue(isinstance(usr_prf, UserProfile))
		self.assertEqual(usr_prf.__unicode__(), usr_prf.user.username)
		self.assertEqual(usr_prf.first_Name,'test user1 fn')
		self.assertEqual(usr_prf.pickupArrangements,'car')
		

	def test_tool_register_model(self):
		
		self.assertEqual(self.toolRegister.nameOfTheTool,'test_hammer')
		self.assertEqual(self.toolRegister.addressOfTheTool,'Rustic Village')
		self.assertEqual(self.toolRegister.statusOfTheTool,'Available')
		self.assertEqual(self.toolRegister.categoryOfTheTool,'Hammer')
		self.assertEqual(self.toolRegister.conditionOfTheTool,'Good')
		self.assertEqual(self.toolRegister.toolDescription,'Its a nice hammer')
		self.assertEqual(self.toolRegister.userProfile,self.testUserProfile)
		self.assertEqual(self.toolRegister.userProfile.user,self.testUser)

	def test_tool_request_model(self):
		self.assertEqual(self.toolRequest.toolId,self.toolRegister)
		self.assertEqual(self.toolRequest.requester_id,'1')
		self.assertEqual(self.toolRequest.requestedFromDate,date.today())
		self.assertEqual(self.toolRequest.requestedToDate,date.today())
		self.assertEqual(self.toolRequest.requestStatus,'1')
		
	def test_tool_borrowed_model(self):
		self.assertEqual(self.toolBorrowed.toolId,self.toolRegister)
		self.assertEqual(self.toolBorrowed.requestId,self.toolRequest)
		self.assertEqual(self.toolBorrowed.borrowerId,'2')
		self.assertEqual(self.toolBorrowed.notified,1)

	def test_tool_rejected_model(self):
		self.assertEqual(self.toolRejected.toolId,self.toolRegister)
		self.assertEqual(self.toolRejected.requestId,self.toolRequest)
		self.assertEqual(self.toolRejected.requesterId,'1')
		self.assertEqual(self.toolRejected.rejectionReason,'Rejected')
		self.assertEqual(self.toolRejected.notified,1)

	def test_tool_Return_model(self):
		self.assertEqual(self.toolReturn.toolId,self.toolRegister)
		self.assertEqual(self.toolReturn.requestId,self.toolRequest)
		self.assertEqual(self.toolReturn.note,'Thank You')
		self.assertEqual(self.toolReturn.rating,'1')

# Create your View tests here.
class viewsTests(TestCase):

		# Initial Setup for testing the views.
	def setUp(self):
		self.client = Client()
		self.theUser = User.objects.create_user('test_user1','123','test_user1@toolshare.com')
		self.shareZone = ShareZone.objects.create(
			zipCode=14623,
			has_CommunityShed=1,
			CommunityShedLocation='Rustic'
			)
		self.testUserProfile = UserProfile.objects.create(
			user=self.theUser,
			first_Name='test user1 fn',
			last_Name='test user1 ln',
			address='123 Street st.',
			zipCode=14623,
			pickupArrangements='car',
			date='2015-10-10',
			ShareZone=self.shareZone,
			request=1,
			is_admin=1
			)
		self.ToolRegister = ToolsRegister.objects.create(
			userProfile = self.testUserProfile,
    		nameOfTheTool = 'test hammer',
    		addressOfTheTool = 'Rustic',
    		statusOfTheTool = 'Available',
    		categoryOfTheTool = 'Hammer',
    		conditionOfTheTool = 'Good',
    		toolDescription = 'Hammer',
    		image = tempfile.NamedTemporaryFile(suffix=".png").name
			)
		
		self.ToolRequest = ToolRequest.objects.create(
 			toolId = self.ToolRegister,
    		requester_id = '1',
    		requestedFromDate = date.today(),
    		requestedToDate = date.today(),
    		requestStatus = 1
			)
		self.client.force_login(User.objects.get_or_create(username='test_user1')[0])



		# Test if the login page can be accessed.
	def test_login_access(self):
		
		response = self.client.get('/')
		self.assertTemplateUsed(response,'registration/login.html')
		self.assertEqual(response.status_code,200)

		# Test if the login_failure form contains the right username.
	def test_login_failure(self):
		response = self.client.post('/',{'username':'test_user1','password':'123'})
		self.assertContains(response, "test_user2", 0, 200)
		

		# Test if the login_sucess form contains the right username.
	def test_login_success(self):
		response = self.client.post('/',{'username':'test_user1','password':'123'})
		self.assertContains(response, "test_user1", 1, 200)


	def test_access_my_profile(self):
		resp = self.client.get('/myProfile/')
		self.assertTemplateUsed(resp,'registration/myProfile.html')
		self.assertEqual(resp.status_code, 200)

	
	def test_access_home(self):
		response = self.client.get('/home/')
		self.assertTemplateUsed(response,'home.html')
		self.assertEqual(response.status_code, 200)

	def test_access_add_new_tool(self):
		response = self.client.get('/addNewTool/')
		self.assertTemplateUsed(response,'ToolManagement/addNewTool.html')
		self.assertEqual(response.status_code, 200)

	def test_access_manage_my_tools(self):
		response = self.client.get('/manageMyTools/')
		self.assertTemplateUsed(response,'ToolManagement/manageTheRegisteredTool.html')
		self.assertEqual(response.status_code, 200)

	def test_access_borrow_tools(self):
		response = self.client.get('/borrowTools/')
		self.assertTemplateUsed(response,'ToolManagement/borrowTools.html')
		self.assertEqual(response.status_code, 200)

	def test_access_update_tool(self):
		session = self.client.session
		session['ToolId'] = 1
		session.save()
		response = self.client.get('/toolUpdate/')
		self.assertTemplateUsed(response,'ToolManagement/toolUpdate.html')
		self.assertEqual(response.status_code, 200)

	def test_access_shareZone(self):
		response = self.client.get('/ShareZone/')
		print(response)
		self.assertTemplateUsed(response,'ShareZone.html')
		self.assertEqual(response.status_code, 200)

# Create your form tests here.
class formTests(TestCase):

	def setUp(self):
		self.client = Client()
		self.theUser = User.objects.create_user('test_user1','123','test_user1@toolshare.com')
		self.shareZone = ShareZone.objects.create(
			zipCode=14623,
			has_CommunityShed=1,
			CommunityShedLocation='Rustic'
			)
		self.testUserProfile = UserProfile.objects.create(
			user=self.theUser,
			first_Name='test user1 fn',
			last_Name='test user1 ln',
			address='123 Street st.',
			zipCode=14623,
			pickupArrangements='car',
			date='2015-10-10',
			ShareZone=self.shareZone,
			request=1,
			is_admin=1
			)
		self.ToolRegister = ToolsRegister.objects.create(
			userProfile = self.testUserProfile,
    		nameOfTheTool = 'test hammer',
    		addressOfTheTool = 'Rustic',
    		statusOfTheTool = 'Available',
    		categoryOfTheTool = 'Hammer',
    		conditionOfTheTool = 'Good',
    		toolDescription = 'Hammer',
    		image = tempfile.NamedTemporaryFile(suffix=".png").name
			)
		
		self.ToolRequest = ToolRequest.objects.create(
 			toolId = self.ToolRegister,
    		requester_id = '1',
    		requestedFromDate = date.today(),
    		requestedToDate = date.today(),
    		requestStatus = 1
			)
		self.client.force_login(User.objects.get_or_create(username='test_user1')[0])


	def test_registration_form_date_invalid(self):
		form = RegistrationForm(data={'username':'test_user1','email':'test_user1@toolshare.com',
			'password1':'123','password2':'123','first_Name':'test user1 fn',
			'last_Name' :'test user1 ln',
			'address' :'123 Street st.',
			'zipCode' :14623,
			'pickupArrangements':'car',
			'date':12/12/1944
			})
		self.assertFalse(form.is_valid())

	def test_registration_form_valid(self):
		form = RegistrationForm(data={'username':'test_user9','email':'test_user1@toolshare.com',
			'password1':'123','password2':'123','first_Name':'test user1 fn',
			'last_Name' :'test user1 ln',
			'address' :'123 Street st.',
			'zipCode' :14623,
			'pickupArrangements':'car',
			'date':'1944-12-12'
			})
		self.assertTrue(form.is_valid())

	def test_Tool_Entry_form_image_invalid(self):
		form = ToolEntryForm(data={
		'nameOfTheTool' : 'Test Hammer',
    	'addressOfTheTool' : 'Home',
    	'statusOfTheTool' : 'Available',
    	'categoryOfTheTool' : 'Hammer',
    	'conditionOfTheTool' : 'Good',
    	'toolDescription' : 'Hammer'
    	})
		print(form.errors)
		self.assertFalse(form.is_valid())
		#self.assertEquals(form.errors,'{\'image\': [\'This field is required.\']}')

	def test_Tool_Entry_form_addr_invalid(self):
		form = ToolEntryForm(data={
		'nameOfTheTool' : 'Test Hammer',
    	'addressOfTheTool' : 'RR',
    	'statusOfTheTool' : 'Available',
    	'categoryOfTheTool' : 'Hammer',
    	'conditionOfTheTool' : 'Good',
    	'toolDescription' : 'Hammer'
    	})
		print(form.errors)
		self.assertFalse(form.is_valid())

	def test_Tool_Entry_form_valid(self):
		form = ToolEntryForm(data={
		'nameOfTheTool' : 'Test Hammer',
    	'addressOfTheTool' : 'RR',
    	'statusOfTheTool' : 'Available',
    	'categoryOfTheTool' : 'Hammer',
    	'conditionOfTheTool' : 'Good',
    	'toolDescription' : 'Hammer',
    	'image' : tempfile.NamedTemporaryFile(suffix=".png").name
    	})
		print(form.errors)
		self.assertFalse(form.is_valid())





