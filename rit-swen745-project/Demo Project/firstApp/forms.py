from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from firstApp.models import *

class RegistrationForm(forms.Form):
    username = forms.RegexField(
        regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
        label=_("Username"), error_messages={
            'invalid': _("This value must contain only letters, numbers and underscores.")
        }
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
        label=_("Email Address")
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
        label=_("Password")
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
        label=_("Password (again)")
    )
    first_Name = forms.CharField(
        widget=forms.TextInput(attrs=dict(required=True, max_length=25)),
        label=_("First Name")
    )
    last_Name = forms.CharField(
        widget=forms.TextInput(attrs=dict(required=True, max_length=25)),
        label=_("Last Name")
    )
    affiliation = forms.CharField(
        widget=forms.TextInput(attrs=dict(required=True, max_length=25)),
        label=_("Affiliation")
    )

    class Meta:
        model = UserProfile
        exclude = ('user')

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists."))

    # def clean(self):
    #     if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
    #         if self.cleaned_data['password1'] != self.cleaned_data['password2']:
    #             raise forms.ValidationError(_("The two password fields did not match."))
    #     return self.cleaned_data

    def getUsername(self):
        return self.username

    def getEmail(self):
        return self.email

    def getPassword(self):
        return self.password1

    def clean(self):
        pass
        try:
            username=self.cleaned_data['first_Name']
        except KeyError:
            raise forms.ValidationError('Please enter your first name')
        try:
            username=self.cleaned_data['last_Name']
        except KeyError:
            raise forms.ValidationError('Please enter your last name')
        try:
            username=self.cleaned_data['affiliation']
        except KeyError:
            raise forms.ValidationError('Please enter your affiliation')
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data

class DocSubmitForm(forms.Form):
    doc_format_choices = (
        ('PDF', 'PDF'),
        ('Word Document', 'Word Document'),
    )
    doc_title = forms.CharField(max_length=100, label=_("Document Title"))
    submitter_email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=70)), label=_("Submitter Email Address"))
    doc_version = forms.IntegerField(label=_("Document Version"))
    doc_format = forms.ChoiceField(choices=doc_format_choices, required=True, label=_("Document Format"))
    document = forms.FileField(label=_("Upload Document"))

    def clean(self):
        try:
            document=self.cleaned_data['document']
        except KeyError:
            #self._errors['document'] = [u'Please upload a document.']
            raise forms.ValidationError(_('Please upload a document.'),code='invalid')
        if self.cleaned_data['doc_format'] == 'PDF':
            if '.pdf' not in self.cleaned_data['document'].name:
                #self.add_error('document', "Please upload a pdf document or change the Document Format field to 'Word Document'.")
                raise forms.ValidationError(_("Please upload a pdf document or change the Document Format field to 'Word Document'."))
        elif self.cleaned_data['doc_format'] == 'Word Document':
            if not self.cleaned_data['document'].name.endswith('.docx') and not self.cleaned_data['document'].name.endswith('.doc'):
                #self.add_error('document', "Please upload a word document or change the Document Format field to 'PDF'.")
                raise forms.ValidationError(_("Please upload a word document or change the Document Format field to 'PDF'."))
        else:
            #self.add_error('document', "Please upload a pdf or word document.")
            raise forms.ValidationError(_("Please upload a pdf or word document."))
        return self.cleaned_data

class LinkForm(forms.Form):
    contributor_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Name',
        }),
        required=False,
        label=_("Contributor Name")
    )
    contributor_email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Email',
        }),
        required=False,
        label=_("Contributor Email")
    )

class UserProfileForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs=dict(max_length=30)),
        label=_("Email Address")
    )
    first_Name = forms.CharField(
        widget=forms.TextInput(attrs=dict(max_length=25)),
        label=_("First Name")
    )
    last_Name = forms.CharField(
        widget=forms.TextInput(attrs=dict(max_length=25)),
        label=_("Last Name")
    )
    affiliation = forms.CharField(
        widget=forms.TextInput(attrs=dict(max_length=25)),
        label=_("Affiliation")
    )

class DeadlineForm (forms.Form):
    to_date=forms.DateField()
    from_date=forms.DateField()
    type = forms.ChoiceField(choices=deadline_type_choices, widget=forms.RadioSelect())


class ReviewRatingForm(forms.Form):
    rating_choices = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )

    review = forms.CharField(
        widget=forms.TextInput(attrs=dict(max_length=150)),
        label=_("Review")
    )

    rating = forms.ChoiceField(choices=rating_choices, required=True, label=_("Rating"))

    paper_summary = forms.CharField(
        widget=forms.Textarea(attrs=dict(max_length=500)),
        label=_("Paper Summary")
    )

    doc_id = forms.CharField(
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
        label=_("doc_id")
    )

class TemplateForm(forms.Form):
    template_type = forms.ChoiceField(choices=template_type_choices, required=True, label=_("Type"))
    template_message = forms.CharField(
        widget=forms.Textarea(attrs=dict(max_length=500)),
        label=_("Message")
    )