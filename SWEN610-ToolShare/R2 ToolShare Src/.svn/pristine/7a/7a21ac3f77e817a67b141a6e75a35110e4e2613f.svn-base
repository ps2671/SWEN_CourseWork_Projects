from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from firstApp.models import *
#from bootstrap3_datetime.widgets import DateTimePicker
from firstApp.models import ToolsRegister
from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib.auth.forms import PasswordChangeForm


class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict( max_length=30,min_length=8)),
                                label=_("Username"), error_messages={
            'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(max_length=30)), label=_("Email address"),)
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict( max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict( max_length=30, render_value=False)),
        label=_("Password (again)"))

    #first_Name = forms.CharField(max_length=25)
    first_Name = forms.RegexField(regex=r'^[a-zA-Z]*$', max_length=64, error_messages={'invalid':_("Only alphabetical characters are allowed")})
    last_Name = forms.RegexField(regex=r'^[a-zA-Z]*$', max_length=25,error_messages={'invalid':_("Only alphabetical characters are allowed")})
    zipCode = forms.RegexField(regex="\d{5}([ \-]\d{4})?", error_messages={'invalid':_("Please enter a valid US zipcode.")})
    #notificationFrequency = forms.IntegerField()-->
    #address = forms.CharField(max_length=64)
    address = forms.RegexField(regex=r'^[a-zA-Z0-9_ ]*$', max_length=100,
                               error_messages={'invalid': _("Please Enter a valid Address, No symbols are allowed.")})
    #address = forms.RegexField(regex=r'^[a-zA-Z0-9]*$',max_length=25, error_messages={'invalid':_("Please Enter a valid Adress, No symbols are allowed.")})
    pickupArrangements = forms.CharField(max_length=25)
    #date = forms.DateField(
        #widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                               "pickTime": False}))
    date = forms.DateField(label='Birthday',
                    widget=forms.TextInput(attrs={'placeholder': 'mm/dd/yyyy'}))
    #function for checking user age under 13 in Registration page
    def clean_date(self):
        dob = self.cleaned_data.get('date')
        age = (datetime.now().date() - dob).days/365
        if age < 13:
            raise forms.ValidationError('Must be at least 13 years old to register')
        return dob

    class Meta:
        model = UserProfile
        exclude = ('user')

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    '''def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 in self.cleaned_data and password2 in self.cleaned_data:
            if password1 != password2:
                raise forms.ValidationError("The two password fields did not match.")
        return self.cleaned_data'''

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2

    '''def clean_age(self):
        birthdate = self.cleaned_data.get['birthdate']
        #a=13
        if birthdate != 13:
            raise forms.ValidationError("Your must be older then 13")
        return birthdate'''
# check if the email is exist in DB that enter by user
    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError('This email already exist')
        return self.cleaned_data['email']

    def getUsername(self):
        return self.username

    def getEmail(self):
        return self.email

    def getPassword(self):
        return self.password1

class ToolEntryForm(forms.Form):
    categoryChoices = (
        ('Axe', 'Axe'),
        ('Hammer', 'Hammer'),
        ('Screw', 'Screw'),
        ('Shovel', 'Shovel'),
    )
    conditionChoices = (
        ('Good', 'Good'),
        ('Bad', 'Bad'),
        ('Ok', 'ok'),
    )
    statusChoices = (
        ('Available', 'Available'),
        ('UnAvailable', 'UnAvailable'),
    )
    toolAvailChoices = (
        ('Home', 'Home'),
        ('Community_Shed', 'Community Shed'),
    )
    toolAvailChoices1 = (
        ('Home', 'Home'),
        ('', '')
    )
    nameOfTheTool = forms.CharField(required=True, max_length=100)
    addressOfTheTool = forms.ChoiceField(required=False,choices=toolAvailChoices,initial='Home')
    # addressOfTheTool1 = forms.ChoiceField(choices=toolAvailChoices1,required=True)
    statusOfTheTool = forms.ChoiceField(choices=statusChoices, required=True)
    categoryOfTheTool = forms.ChoiceField(choices=categoryChoices, required=True)
    conditionOfTheTool = forms.ChoiceField(choices=conditionChoices, required=True)
    toolDescription = forms.CharField(max_length=500, required=True)
    # this function for checking file format in image upload
    def validate_file_extension(self):
        import os
        ext = os.path.splitext(self.name)[1]
        valid_extensions = ['.jpg', '.png', '.jpeg', 'gif']
        if not ext in valid_extensions:
            raise forms.ValidationError('File not supported!')

    image = forms.FileField(validators=[validate_file_extension], required=True)

    #checking image size
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image._size > 2 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 2mb )")
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")

class ToolUpdateForm(forms.Form):
    categoryChoices = (
        ('Axe', 'Axe'),
        ('Hammer', 'Hammer'),
        ('Screw', 'Screw'),
        ('Shovel', 'Shovel'),
    )
    conditionChoices = (
        ('Good', 'Good'),
        ('Bad', 'Bad'),
        ('Ok', 'ok'),
    )
    statusChoices = (
        ('Available', 'Available'),
        ('UnAvailable', 'UnAvailable'),
    )
    toolAvailChoices = (
        ('Home', 'Home'),
        ('Community_Shed', 'Community Shed'),
    )
    toolAvailChoices1 = (
        ('Home', 'Home'),
        ('', ''),
    )
    nameOfTheTool = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    addressOfTheTool = forms.ChoiceField(choices=toolAvailChoices, required=False)
    #addressOfTheTool1 = forms.ChoiceField(choices=toolAvailChoices1, required=True)
    statusOfTheTool = forms.ChoiceField(choices=statusChoices, required=True)
    categoryOfTheTool = forms.ChoiceField(choices=categoryChoices, required=True)
    conditionOfTheTool = forms.ChoiceField(choices=conditionChoices, required=True)
    toolDescription = forms.CharField(max_length=500)
    # this function for checking file format in image upload
    def validate_file_extension(self):
        import os
        ext = os.path.splitext(self.name)[1]
        valid_extensions = ['.jpg', '.png', '.jpeg', 'gif']
        if not ext in valid_extensions:
            raise forms.ValidationError('File not supported!')

    image = forms.FileField(required=False, validators=[validate_file_extension])
    # checking image size
    # def clean_image(self):
     #   image = self.cleaned_data.get('image')
      #  if image:
       #     if image._size > 2 * 1024 * 1024:
        #        raise forms.ValidationError("Image file too large ( > 2mb )")
         #   return image
        #else:
         #   raise ValidationError("Couldn't read uploaded image")


class ToolBorrowForm(forms.Form):
    requester_id = forms.CharField(max_length=100)

class ToolReturnForm(forms.Form):
    ratingChoices = (
        ('5', '5'),
        ('4', '4'),
        ('3', '3'),
        ('2', '2'),
        ('1', '1'),
    )
    note = forms.CharField(max_length=100,required=True)
    rating = forms.ChoiceField(choices=ratingChoices,required=True)

'''def clean(self):
        note1 = self.cleaned_data.get('note')

        if note1:
            self.fields_required(['note'])
        else:
            self.cleaned_data['note'] = ''

        return self.cleaned_data'''

class UserProfileForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(max_length=30)), label=_("Email address"))
    first_Name = forms.RegexField(regex=r'^[a-zA-Z]*$', max_length=64,
                                  error_messages={'invalid': _("Only alphabetical characters are allowed")})
    last_Name = forms.RegexField(regex=r'^[a-zA-Z]*$', max_length=25,
                                 error_messages={'invalid': _("Only alphabetical characters are allowed")})
    zipCode = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}),max_length=5)
    address = forms.RegexField(regex=r'^[a-zA-Z0-9_ ]*$', max_length=100,
                               error_messages={'invalid': _("Please Enter a valid Address, No symbols are allowed.")})
    pickupArrangements = forms.CharField(max_length=25)
    #date = forms.DateField(
    #    widget=DateTimePicker(options={"format": "YYYY-MM-DD",
    #                                   "pickTime": False}))
    date1 = forms.DateField(label='Birthday',widget=forms.DateInput(format = '%m/%d/%Y'))

    # function for checking user age if it more than 13 in update profile page
    def clean_date1(self):
        dob = self.cleaned_data.get('date1')
        age = (datetime.now().date() - dob).days / 365
        if age < 13:
            raise forms.ValidationError('Must be at least 13 years old')
        return dob

    # check if the email is exist in DB that enter by user
    def clean_email(self):
        return self.cleaned_data['email']



class CommunityShedCreation(forms.Form):
    address = forms.RegexField(regex="[a-zA-Z0-9]+$", max_length = 100, error_messages={'invalid':_("Please enter a valid address(only numbers and letters) .")})

class ChangePasswordForm(forms.Form):
    #passwor_check=forms.CharField(
     #   widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Enter your old password"))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Enter a new Password"))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
        label=_("Confirm your new password"))

    #def pass_check(self):
     #p1 = self.cleaned_data.get('passwor_chek')
      #p2 = self.cleaned_data.get('password')
      #if p1!=p2:
       # raise forms.ValidationError('Your old password not right')

    def clean(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        try:
            self.cleaned_data['password1']
        except KeyError:
            raise forms.ValidationError('Please enter the password')
        try:
            self.cleaned_data['password2']
        except KeyError:
            raise forms.ValidationError('Please enter the confirm password')
        try:
             k = self.cleaned_data['password1']
             m = self.cleaned_data['password2']
        except k!=m:
            raise forms.ValidationError('Password not matching')

   #'''def pass_check(self):
     #   p1 = self.cleaned_data['passwor_chek']
      #  p2 = self.cleaned_data['password']
       # if p1!=p2:
        #    raise forms.ValidationError('Your old password not right')'''

class ToFromDateForm(forms.Form):

    fromDate = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'readonly':'readonly','required': 'true'})

    )
    toDate = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'readonly':'readonly'}))

    def clean_date(self):
        d = self.cleaned_data.get['fromDate']
        d2 = self.cleaned_data.get['toDate']
        #age = (datetime.now().date() - dob).days / 365
        #t1=datetime.now()
        if d < datetime.now().date():
            raise forms.ValidationError('you must select new date')
        return d

    '''def _clean_fields(self):
      data = self.cleaned_data
      if data.get('fromDate', None) or (data.get('toDate', None)):
        return data
      else:
        raise forms.ValidationError('Please Enter date.')'''

class RejectionReasonForm(forms.Form):
    rejectionReason = forms.CharField(max_length=500)
    #rejectionForm validation is required
    def clean(self):
        try:
            self.cleaned_data['rejectionReason']
        except KeyError:
            print("it is coming here")
            raise forms.ValidationError('Please specify the rejection reason!')

