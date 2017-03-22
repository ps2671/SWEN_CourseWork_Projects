# Create your views here.
import datetime
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_protect
from django.http import FileResponse, HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from firstApp.forms import *
from firstApp.models import *
from firstApp import signals
from django.forms import *
from django.forms.formsets import formset_factory
from Demo.settings import MEDIA_ROOT
from django.db.models import Count

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_Name'],
                last_name=form.cleaned_data['last_Name']
            )

            userProfile=UserProfile(
                user=user,
                affiliation=form.cleaned_data['affiliation']
            )
            user.save()
            userProfile.save()
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm

    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response(
        'registration/register.html',
        variables,
    )


def register_success(request):
    return render_to_response(
        'registration/register_success.html',
    )


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def home(request):

    perm_can_review_doc = False
    perm_can_edit_rev_req = False
    perm_can_submit_paper  = False

    if request.user.has_perm("firstApp.add_documentsubmission"):
        perm_can_submit_paper = True

    if request.user.has_perm("firstApp.add_review") and request.user.has_perm("firstApp.change_review"):
        perm_can_review_doc = True
    if request.user.has_perm("firstApp.change_request_paper_review"):
        perm_can_edit_rev_req = True

    return render_to_response(
        'home.html', {
            'user': request.user,
            'perm_can_review_doc': perm_can_review_doc,
            'perm_can_edit_rev_req': perm_can_edit_rev_req,
            'perm_can_submit_paper':perm_can_submit_paper
        }
    )


@login_required
def myProfile(request):
    perm_can_review_doc = False
    perm_can_edit_rev_req = False
    perm_can_submit_paper  = False

    if request.user.has_perm("firstApp.add_documentsubmission"):
        perm_can_submit_paper = True


    if request.user.has_perm("firstApp.add_review") and request.user.has_perm("firstApp.change_review"):
        perm_can_review_doc = True
    if request.user.has_perm("firstApp.change_request_paper_review"):
        perm_can_edit_rev_req = True

    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    context = {
        'user':user,
        'userProfile':userProfile,
        'perm_can_review_doc': perm_can_review_doc,
        'perm_can_edit_rev_req': perm_can_edit_rev_req,
        'perm_can_submit_paper':perm_can_submit_paper
    }

    return render_to_response(
        'registration/myProfile.html',
        context
    )


@login_required
def updateProfile(request):
    perm_can_review_doc = False
    perm_can_edit_rev_req = False
    perm_can_submit_paper  = False

    if request.user.has_perm("firstApp.add_documentsubmission"):
        perm_can_submit_paper = True


    if request.user.has_perm("firstApp.add_review") and request.user.has_perm("firstApp.change_review"):
        perm_can_review_doc = True
    if request.user.has_perm("firstApp.change_request_paper_review"):
        perm_can_edit_rev_req = True

    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    canSendUserAccountSignal = False

    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            # Only change the fields if the data from the from is different
            # than the data from the database
            updated_field_value_dict = {}
            if user.email != form.cleaned_data['email']:
                user.email = form.cleaned_data['email']
                updated_field_value_dict['email'] = user.email
            if user.first_name != form.cleaned_data['first_Name']:
                user.first_name = form.cleaned_data['first_Name']
                updated_field_value_dict['first_name'] = user.first_name
            if user.last_name != form.cleaned_data['last_Name']:
                user.last_name = form.cleaned_data['last_Name']
                updated_field_value_dict['last_name'] = user.last_name
            if userProfile.affiliation != form.cleaned_data['affiliation']:
                userProfile.affiliation = form.cleaned_data['affiliation']
                updated_field_value_dict['affiliation'] = userProfile.affiliation

            # If any of the User fields changed, save the User object
            if ('email' in updated_field_value_dict
                    or 'first_name' in updated_field_value_dict
                    or 'last_name' in updated_field_value_dict):
                canSendUserAccountSignal = True
                user.save()
            # If any of the UserProfile fields changed, save the UserProfile object
            if ('affiliation' in updated_field_value_dict):
                canSendUserAccountSignal = True
                userProfile.save()
            # If any of the User or UserProfile fields changed, send an account
            # update signal to create a notification
            if canSendUserAccountSignal:
                signals.user_account_update_signal.send(
                    sender=None,
                    user_object=user,
                    updated_field_value_dict=updated_field_value_dict
                )

            variables = RequestContext(request, {
                'form': form
            })
            return HttpResponseRedirect('/home/')

    else:
        form = UserProfileForm()
        form.fields['username'].initial = user.username
        form.fields['email'].initial = user.email
        form.fields['first_Name'].initial = user.first_name
        form.fields['last_Name'].initial = user.last_name
        form.fields['affiliation'].initial = userProfile.affiliation

    return render_to_response(
        'registration/Update_Profile.html',
        context_instance = RequestContext(
            request, {
                'form': form,
                'perm_can_review_doc': perm_can_review_doc,
                'perm_can_edit_rev_req': perm_can_edit_rev_req,
                'perm_can_submit_paper':perm_can_submit_paper
            }
       )
    )


@login_required
def viewSubmission(request):
    perm_can_review_doc = False
    perm_can_edit_rev_req = False
    perm_can_submit_paper  = False
    doc_submit_dict={}

    if request.user.has_perm("firstApp.add_documentsubmission"):
        perm_can_submit_paper = True



    if request.user.has_perm("firstApp.add_review") and request.user.has_perm("firstApp.change_review"):
        perm_can_review_doc = True
    if request.user.has_perm("firstApp.change_request_paper_review"):
        perm_can_edit_rev_req = True



    user = request.user
    submitted_docs = DocumentSubmission.objects.filter(submitter=user)
    for doc in submitted_docs:
        doc_contri_list = DocumentContributor.objects.filter(document=doc)
        doc_submit_dict[doc]=doc_contri_list

    if submitted_docs.count() > 0:
        context = {
            'user': user,
            'submitted_docs': submitted_docs,
            'perm_can_review_doc': perm_can_review_doc,
            'perm_can_edit_rev_req': perm_can_edit_rev_req,
            'perm_can_submit_paper':perm_can_submit_paper,
            'doc_submit_dict':doc_submit_dict
        }
    else:
        context = {
            'user': user,
            'perm_can_review_doc': perm_can_review_doc,
            'perm_can_edit_rev_req': perm_can_edit_rev_req,
            'perm_can_submit_paper':perm_can_submit_paper
        }


    # try:
        # submitted_doc = DocumentSubmission.objects.get(submitter=user)
    # except:
        # context = {
            # 'user':user,
            # 'perm_can_review_doc': perm_can_review_doc,
            # 'perm_can_edit_rev_req': perm_can_edit_rev_req
        # }
        # return render_to_response(
            # 'view_submission.html',
            # context
        # )

    # doc_title = submitted_doc.doc_title
    # submitter_email = submitted_doc.submitter_email
    # doc_version = submitted_doc.doc_version
    # doc_format = submitted_doc.doc_format
    # status = submitted_doc.status
    # document = submitted_doc.document

    # context = {
        # 'user':user,
        # 'submitted_doc':submitted_doc,
        # 'doc_title':doc_title,
        # 'submitter_email':submitter_email,
        # 'doc_version':doc_version,
        # 'doc_format':doc_format,
        # 'status':status,
        # 'document':document,
        # 'perm_can_review_doc': perm_can_review_doc,
        # 'perm_can_edit_rev_req': perm_can_edit_rev_req
    # }

    return render_to_response(
        'view_submission.html',
        context
    )


@login_required
def viewPDF(request, id=None):
    perm_can_review_doc = False
    perm_can_edit_rev_req = False
    perm_can_submit_paper  = False

    if request.user.has_perm("firstApp.add_documentsubmission"):
        perm_can_submit_paper = True

    if request.user.has_perm("firstApp.add_review") and request.user.has_perm("firstApp.change_review"):
        perm_can_review_doc = True
    if request.user.has_perm("firstApp.change_request_paper_review"):
        perm_can_edit_rev_req = True

    if request.method == 'GET':
        user = request.user
        submitted_doc = get_object_or_404(DocumentSubmission, submitter_id=user.id, id=id)

        if 'PDF' == submitted_doc.doc_format:
            image_data = open(MEDIA_ROOT+'/'+submitted_doc.document.name, 'rb').read()
            return HttpResponse(image_data, content_type='application/pdf')
        else:
            image_data = open(MEDIA_ROOT+'/'+submitted_doc.document.name, 'rb').read()
            return HttpResponse(image_data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')


@login_required
def docSubmission(request):
    perm_can_review_doc = False
    perm_can_edit_rev_req = False
    perm_can_submit_paper  = False

    if request.user.has_perm("firstApp.add_documentsubmission"):
        perm_can_submit_paper = True


    if request.user.has_perm("firstApp.add_review") and request.user.has_perm("firstApp.change_review"):
        perm_can_review_doc = True
    if request.user.has_perm("firstApp.change_request_paper_review"):
        perm_can_edit_rev_req = True

    # Create the formset, specifying the form and formset we want to use.
    LinkFormSet = formset_factory(LinkForm)

    # Determine whether the system is currently within a paper submission
    # deadline, if any exist
    isWithinDeadline = False
    paperSubmissionDeadlines = Deadline.objects.filter(type='Paper Submit')
    if paperSubmissionDeadlines.count() > 0:
        psDeadline = paperSubmissionDeadlines[0]
        currentDate = datetime.date.today()
        isWithinDeadline = currentDate >= psDeadline.from_date and currentDate <= psDeadline.to_date

    if request.user.has_perm("firstApp.add_documentsubmission"):
        if request.method == 'POST':
            form = DocSubmitForm(request.POST,request.FILES)
            link_formset = LinkFormSet(request.POST)
            variables = RequestContext(request, {
                'form': form,
                'perm_can_submit_paper': True,
                'is_within_deadline': isWithinDeadline,
                'link_formset': link_formset,
                'perm_can_review_doc': perm_can_review_doc,
                'perm_can_edit_rev_req': perm_can_edit_rev_req,
                'perm_can_submit_paper':perm_can_submit_paper
            })

            if form.is_valid() and link_formset.is_valid():
                user = request.user
                documentSubmission=DocumentSubmission(
                    submitter=user,
                    doc_title=form.cleaned_data['doc_title'],
                    submitter_email=form.cleaned_data['submitter_email'],
                    doc_version=form.cleaned_data['doc_version'],
                    doc_format=form.cleaned_data['doc_format'],
                    document=form.cleaned_data['document'],
                )
                documentSubmission.save()

                for link_form in link_formset:
                    contributor_name = link_form.cleaned_data.get('contributor_name')
                    contributor_email = link_form.cleaned_data.get('contributor_email')
                    documentContributor = DocumentContributor(
                        document=documentSubmission,
                        contributor_name=contributor_name,
                        contributor_email=contributor_email
                    )
                    documentContributor.save()

                return render_to_response('submission_success.html', variables)
        else:
            form = DocSubmitForm()
            link_formset = LinkFormSet()

            variables = RequestContext(request, {
                'form': form,
                'perm_can_submit_paper': True,
                'is_within_deadline': isWithinDeadline,
                'link_formset': link_formset,
                'perm_can_review_doc': perm_can_review_doc,
                'perm_can_edit_rev_req': perm_can_edit_rev_req,
                'perm_can_submit_paper':perm_can_submit_paper
            })

    else:
        form = DocSubmitForm()
        link_formset = LinkFormSet()

        variables = RequestContext(request, {
            'form': form,
            'perm_can_submit_paper': False,
            'is_within_deadline': isWithinDeadline,
            'link_formset': link_formset,
            'perm_can_review_doc': perm_can_review_doc,
            'perm_can_edit_rev_req': perm_can_edit_rev_req,
            'perm_can_submit_paper':perm_can_submit_paper
        })

    return render_to_response(
        'submission.html',
        variables
    )


@login_required
def mark_as_read(request, id=None):
    if request.method == 'POST':
        notification = get_object_or_404(
            Notification, recipient=request.user, id=id)
        notification.mark_as_read()

    return live_all_notification_list(request)


@login_required
def live_unread_notification_count(request):
    if not request.user.is_authenticated():
        data = {'unread_count':0}
    else:
        data = {
            'unread_count': request.user.notifications.unread().count(),
        }
    return JsonResponse(data)


@login_required
def live_all_notification_list(request):
    if not request.user.is_authenticated():
        data = {
           'unread_count':0,
           'all_list':[]
        }
        return JsonResponse(data)

    generatePaperSubmissionReminders()
    generateReviewListSubmissionReminder()
    generateReviewSubmissionReminderPCM()

    try:
        num_to_fetch = request.GET.get('max', 10)  # If they don't specify, make it 10.
        num_to_fetch = int(num_to_fetch)
        num_to_fetch = max(1, num_to_fetch)  # if num_to_fetch is negative, force at least one fetched notifications
        num_to_fetch = min(num_to_fetch, 100)  # put a sane ceiling on the number retrievable
    except ValueError:
        num_to_fetch = 10  # If casting to an int fails, just make it 10.

    all_list = []

    for n in request.user.notifications.all()[0:num_to_fetch]:
        struct = model_to_dict(n)
        if n.message:
            struct['message'] = str(n.message)
        all_list.append(struct)
    data = {
        'unread_count': request.user.notifications.unread().count(),
        'all_list': all_list
    }

    return JsonResponse(data)

def generatePaperSubmissionReminders():
    currentDate = datetime.date.today()
    tomorrowsDate = currentDate + datetime.timedelta(days=1)
    paperDeadlines = Deadline.objects.filter(type='Paper Submit')
    for deadline in paperDeadlines:
        # If one day before end of deadline, then proceed
        if currentDate == (deadline.to_date - datetime.timedelta(days=1)):
            # Get all authors with no submissions. An author has the permission
            # to add document submissions
            authorPermission = Permission.objects.get(codename='add_documentsubmission')
            allAuthorsWithNoSubmissions = User.objects.filter(Q(user_permissions=authorPermission)).filter(documentsubmission__isnull=True)
            # For each author, get their paper submission reminders from today.
            # If they don't have any such reminders from today, then generate a
            # paper submission reminder for them
            for auth in allAuthorsWithNoSubmissions:
                authPaperRemindersToday = auth.notifications.filter(event_type='PAPER_SUBMISSION_REMINDER', created_date__range=(currentDate, tomorrowsDate))
                if authPaperRemindersToday.count() == 0:
                    paperReminder = Notification(event_type='PAPER_SUBMISSION_REMINDER', recipient=auth, message='Paper Submission is due tomorrow')
                    paperReminder.save()

        if currentDate == deadline.to_date:
            authorPermission = Permission.objects.get(codename='add_documentsubmission')
            allAuthorsWithNoSubmissions = User.objects.filter(Q(user_permissions=authorPermission)).filter(documentsubmission__isnull=True)
            for auth in allAuthorsWithNoSubmissions:
                authPaperRemindersToday = auth.notifications.filter(event_type='PAPER_SUBMISSION_REMINDER',created_date__range=(currentDate, tomorrowsDate))
                if authPaperRemindersToday.count() == 0:
                    paperReminder = Notification(event_type='PAPER_SUBMISSION_REMINDER', recipient=auth, message='Paper Submission is due today')
                    paperReminder.save()

def generateReviewListSubmissionReminder():
    currentDate = datetime.date.today()
    tomorrowsDate = currentDate + datetime.timedelta(days=1)
    reviewlistDeadlines = Deadline.objects.filter(type='Review List')
    for deadline in reviewlistDeadlines:
        if currentDate == (deadline.to_date - datetime.timedelta(days=1)):
            PCMPermission = Permission.objects.get(codename='add_request_paper_review')
            pcmreviewreminder = User.objects.filter(Q(groups__permissions=PCMPermission))
            for pcms in pcmreviewreminder:
                pcmreviewtoday = pcms.notifications.filter(event_type='PCM_SUBMIT_REVIEW_LIST',created_date__range=(currentDate, tomorrowsDate))
                if pcmreviewtoday.count() == 0:
                    reviewtoday = Notification(event_type='PCM_SUBMIT_REVIEW_LIST',recipient =pcms , message = 'Tomorrow is the last day to submit the review list')
                    reviewtoday.save()
        if currentDate==deadline.to_date:
            PCMPermission = Permission.objects.get(codename='add_request_paper_review')
            pcmreviewreminder = User.objects.filter(Q(groups__permissions=PCMPermission))
            for pcms in pcmreviewreminder:
                pcmreviewtoday = pcms.notifications.filter(event_type='PCM_SUBMIT_REVIEW_LIST',created_date__range=(currentDate, tomorrowsDate))
                if pcmreviewtoday.count() == 0:
                    reviewtoday = Notification(event_type='PCM_SUBMIT_REVIEW_LIST', recipient=pcms, message='Today is the last day to submit the review list')
                    reviewtoday.save()


def generateReviewSubmissionReminderPCM():
    currentDate = datetime.date.today()
    tomorrowsDate = currentDate + datetime.timedelta(days=1)
    reviewlistDeadlines = Deadline.objects.filter(type='Submit Review')
    for deadline in reviewlistDeadlines:
        if currentDate == (deadline.to_date - datetime.timedelta(days=1)):
            PCMPermission = Permission.objects.get(codename='add_review')
            pcmfinalreviewreminder = User.objects.filter(Q(groups__permissions=PCMPermission))
            for pcms in pcmfinalreviewreminder:
                pcmfinalreviewtoday = pcms.notifications.filter(event_type='PCM_SUBMIT_REVIEW',created_date__range=(currentDate, tomorrowsDate))
                if pcmfinalreviewtoday.count() == 0:
                    finalreviewtoday = Notification(event_type='PCM_SUBMIT_REVIEW', recipient=pcms, message='Tomorrow is the last day to submit or edit the reviews')
                    finalreviewtoday.save()
        if currentDate == deadline.to_date:
            PCMPermission = Permission.objects.get(codename='add_review')
            pcmfinalreviewreminder = User.objects.filter(Q(groups__permissions=PCMPermission))
            for pcms in pcmfinalreviewreminder:
                pcmfinalreviewtoday = pcms.notifications.filter(event_type='PCM_SUBMIT_REVIEW',created_date__range=(currentDate, tomorrowsDate))
                if pcmfinalreviewtoday.count() == 0:
                    finalreviewtoday = Notification(event_type='PCM_SUBMIT_REVIEW', recipient=pcms, message='Today is the last day to submit or edit the reviews')
                    finalreviewtoday.save()


# To view all submissions only allowed for PCM & PCC.
@login_required
def viewAllSubmissions(request):
    # To check for permissions for PCMs and PCC.
    perm_can_review_doc = False
    perm_can_edit_rev_req = False
    perm_can_submit_paper  = False
    isWithinDeadline = False
    viewPapersbyPCMDeadlines = Deadline.objects.filter(type='Review List')
    if viewPapersbyPCMDeadlines.count() > 0:
        psDeadline = viewPapersbyPCMDeadlines[0]
        currentDate = datetime.date.today()
        isWithinDeadline = currentDate >= psDeadline.from_date and currentDate <= psDeadline.to_date

    if request.user.has_perm("firstApp.add_documentsubmission"):
        perm_can_submit_paper = True


    if request.user.has_perm("firstApp.add_review") and request.user.has_perm("firstApp.change_review"):
        perm_can_review_doc = True
    if request.user.has_perm("firstApp.change_request_paper_review"):
        perm_can_edit_rev_req = True

    user = request.user
    try:
        all_doc_submissions = DocumentSubmission.objects.all()
        requested_doc_submissions = Request_Paper_Review.objects.filter(reviewer=user)
        req_docs_id=[]
        docs_to_view=[]

        for doc in requested_doc_submissions:
            print(doc.document.id)
            req_docs_id.append(doc.document.id)

        # for doc in req_docs_id:
        #     #print(doc)

        for doc in all_doc_submissions:
            print(doc)
            if doc.id not in req_docs_id:
                docs_to_view.append(doc)

        # for doc in docs_to_view:
        #     print("gsfdshf")
        #     print(doc)



    except:
        context = {
            'user':user,
            'perm_can_review_doc': perm_can_review_doc,
            'perm_can_edit_rev_req': perm_can_edit_rev_req,
            'perm_can_submit_paper':perm_can_submit_paper,
            'is_within_deadline': isWithinDeadline
        }
        return render_to_response(
            'pcm_views/viewAllSubmissions.html',
            context
        )
    context = {
        'user':user,
        'all_doc_submissions':all_doc_submissions,
        'requested_doc_submissions':req_docs_id,
        'perm_can_review_doc': perm_can_review_doc,
        'perm_can_edit_rev_req': perm_can_edit_rev_req,
        'perm_can_submit_paper':perm_can_submit_paper,
        'is_within_deadline': isWithinDeadline
    }

    # return render_to_response(
    #     'pcm_views/viewAllSubmissions.html',
    #     context
    # )

    return render_to_response(
        'pcm_views/viewAllSubmissions.html',
        context_instance = RequestContext(
            request, context
       )
    )


# To preview paper and request papers to review allowed for PCM & PCC.
@login_required
def requestPaperToReview(request):

    # To check for permissions for PCMs and PCC.
    perm_can_review_doc = False
    perm_can_edit_rev_req = False
    perm_can_submit_paper  = False

    if request.user.has_perm("firstApp.add_documentsubmission"):
        perm_can_submit_paper = True


    if request.user.has_perm("firstApp.add_review") and request.user.has_perm("firstApp.change_review"):
        perm_can_review_doc = True
    if request.user.has_perm("firstApp.change_request_paper_review"):
        perm_can_edit_rev_req = True

    user = request.user




    if request.method == 'POST' and 'previewDoc' in request.POST:
        print('POST')
        if request.POST.get('document', False):
            doc_id = request.POST['document']
            print(doc_id)
            doc = DocumentSubmission.objects.get(id=doc_id)
            doc_name = doc.document.name
            doc_format = doc.doc_format

            context = {
                'user':user,
                'doc':doc,
                'doc_name':doc_name,
                'doc_format':doc_format,
                'perm_can_review_doc': perm_can_review_doc,
                'perm_can_edit_rev_req': perm_can_edit_rev_req,
                'perm_can_submit_paper':perm_can_submit_paper
            }

        if 'PDF' == doc_format:
            image_data = open(MEDIA_ROOT+'/'+doc_name, 'rb').read()
            return HttpResponse(image_data, content_type='application/pdf')
        else:
            image_data = open(MEDIA_ROOT+'/'+doc_name, 'rb').read()
            return HttpResponse(image_data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

    elif request.method == 'POST' and 'acceptRequest' in request.POST:
        if request.POST.get('document', False):

            doc_id = request.POST['document']
            doc = DocumentSubmission.objects.get(id=doc_id)
            doc_name = doc.document.name
            doc_format = doc.doc_format

            request_Paper_Review = Request_Paper_Review(
                document=doc,
                reviewer=user,
                status='Pending'
            )

            request_Paper_Review.save()

            context = {
                'user':user,
                'req_review_msg':True,
                'doc':doc,
                'doc_name':doc_name,
                'doc_format':doc_format,
                'perm_can_review_doc': perm_can_review_doc,
                'perm_can_edit_rev_req': perm_can_edit_rev_req,
                'perm_can_submit_paper':perm_can_submit_paper
            }
            return render_to_response(
                'request_review_sucess.html',
                context
            )


# To view all submissions only allowed for PCM & PCC.
@login_required
def viewRevReqStatus(request):

    # To check for permissions for PCMs and PCC.
    perm_can_review_doc = False
    perm_can_edit_rev_req = False
    perm_can_submit_paper  = False

    if request.user.has_perm("firstApp.add_documentsubmission"):
        perm_can_submit_paper = True


    if request.user.has_perm("firstApp.add_review") and request.user.has_perm("firstApp.change_review"):
        perm_can_review_doc = True
    if request.user.has_perm("firstApp.change_request_paper_review"):
        perm_can_edit_rev_req = True

    user = request.user
    try:
        requested_doc_submissions = Request_Paper_Review.objects.filter(reviewer=user)

        context = {
            'user':user,
            'requested_doc_submissions':requested_doc_submissions,
            'perm_can_review_doc': perm_can_review_doc,
            'perm_can_edit_rev_req': perm_can_edit_rev_req,
            'perm_can_submit_paper':perm_can_submit_paper
        }

        return render_to_response(
            'pcm_views/viewRevReqStatus.html',
            context_instance = RequestContext(
                request, context
            )
        )

    except:
        context = {
            'user':user,
            'perm_can_review_doc': perm_can_review_doc,
            'perm_can_edit_rev_req': perm_can_edit_rev_req,
            'perm_can_submit_paper':perm_can_submit_paper
        }

        return render_to_response(
            'pcm_views/viewRevReqStatus.html',
            context_instance = RequestContext(
                request, context
            )
        )

# To view and approve/reject review requests only allowed for  PCC.
@login_required
def viewReviewRequests(request):

    perm_can_review_doc = False
    perm_can_edit_rev_req = False
    perm_can_submit_paper  = False

    if request.user.has_perm("firstApp.add_documentsubmission"):
        perm_can_submit_paper = True


    if request.user.has_perm("firstApp.add_review") and request.user.has_perm("firstApp.change_review"):
        perm_can_review_doc = True
    if request.user.has_perm("firstApp.change_request_paper_review"):
        perm_can_edit_rev_req = True

    user = request.user
    requested_doc_submissions = Request_Paper_Review.objects.all()

    context = {
        'user':user,
        'requested_doc_submissions' : requested_doc_submissions,
        'perm_can_review_doc': perm_can_review_doc,
        'perm_can_edit_rev_req': perm_can_edit_rev_req,
        'perm_can_submit_paper':perm_can_submit_paper
     }


    if request.method == 'POST' and 'previewDoc' in request.POST:
        print('POST')
        if request.POST.get('document', False):
            doc_id = request.POST['document']
            print(doc_id)
            doc = DocumentSubmission.objects.get(id=doc_id)
            doc_name = doc.document.name
            doc_format = doc.doc_format

            context = {
                'user':user,
                'doc':doc,
                'doc_name':doc_name,
                'doc_format':doc_format,
                'perm_can_review_doc': perm_can_review_doc,
                'perm_can_edit_rev_req': perm_can_edit_rev_req,
                'perm_can_submit_paper':perm_can_submit_paper
            }

        if 'PDF' == doc_format:
            image_data = open(MEDIA_ROOT+'/'+doc_name, 'rb').read()
            return HttpResponse(image_data, content_type='application/pdf')
        else:
            image_data = open(MEDIA_ROOT+'/'+doc_name, 'rb').read()
            return HttpResponse(image_data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

    elif request.method == 'POST' and 'acceptRequest' in request.POST:
        if request.POST.get('req_id', False):

            req_id = request.POST['req_id']
            req = Request_Paper_Review.objects.get(id=req_id)
            req.status = 'Approved'
            req.save()
            requested_doc_submissions = Request_Paper_Review.objects.all()

            context = {
                'user':user,
                'requested_doc_submissions':requested_doc_submissions,
                'perm_can_review_doc': perm_can_review_doc,
                'perm_can_edit_rev_req': perm_can_edit_rev_req,
                'perm_can_submit_paper':perm_can_submit_paper
            }
            return render_to_response(
                'pcc_views/viewReviewRequests.html',
                context_instance = RequestContext(
                    request, context
                )
            )

    elif request.method == 'POST' and 'rejectRequest' in request.POST:
        if request.POST.get('req_id', False):

            req_id = request.POST['req_id']
            req = Request_Paper_Review.objects.get(id=req_id)
            req.status = 'Rejected'
            req.save()
            requested_doc_submissions = Request_Paper_Review.objects.all()
            context = {
                'user':user,
                'requested_doc_submissions':requested_doc_submissions,
                'perm_can_review_doc': perm_can_review_doc,
                'perm_can_edit_rev_req': perm_can_edit_rev_req,
                'perm_can_submit_paper':perm_can_submit_paper
            }
            return render_to_response(
                'pcc_views/viewReviewRequests.html',
                context_instance = RequestContext(
                    request, context
                )
            )
    else:

        return render_to_response(
            'pcc_views/viewReviewRequests.html',
            context_instance = RequestContext(
                request, context
            )
        )


# To view and update review and rating for documents only allowed for PCMs and PCC.
@login_required
def viewAssignedPapers(request):

    perm_can_review_doc = False
    perm_can_edit_rev_req = False
    perm_can_submit_paper  = False

    if request.user.has_perm("firstApp.add_documentsubmission"):
        perm_can_submit_paper = True


    if request.user.has_perm("firstApp.add_review") and request.user.has_perm("firstApp.change_review"):
        perm_can_review_doc = True
    if request.user.has_perm("firstApp.change_request_paper_review"):
        perm_can_edit_rev_req = True

    user = request.user
    requested_doc_submissions = Request_Paper_Review.objects.filter(reviewer=user,status='Approved')
    user_review = Review.objects.filter(reviewer=user)

    user_doc_ids=[]

    for usr_rev in user_review:
        user_doc_ids.append(usr_rev.document_id)

    for id in user_doc_ids:
        print(id)

    context = {
        'user':user,
        'requested_doc_submissions' : requested_doc_submissions,
        'user_doc_ids':user_doc_ids,
        'perm_can_review_doc': perm_can_review_doc,
        'perm_can_edit_rev_req': perm_can_edit_rev_req,
        'perm_can_submit_paper':perm_can_submit_paper
    }

    if request.method == 'POST' and 'previewDoc' in request.POST:
        print('POST')
        if request.POST.get('document', False):
            doc_id = request.POST['document']

            doc = DocumentSubmission.objects.get(id=doc_id)
            doc_name = doc.document.name
            doc_format = doc.doc_format

            context = {
                'user':user,
                'doc':doc,
                'doc_name':doc_name,
                'doc_format':doc_format,
                'perm_can_review_doc': perm_can_review_doc,
                'perm_can_edit_rev_req': perm_can_edit_rev_req,
                'perm_can_submit_paper':perm_can_submit_paper
            }

        if 'PDF' == doc_format:
            image_data = open(MEDIA_ROOT+'/'+doc_name, 'rb').read()
            return HttpResponse(image_data, content_type='application/pdf')
        else:
            image_data = open(MEDIA_ROOT+'/'+doc_name, 'rb').read()
            return HttpResponse(image_data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

    elif request.method == 'POST' and 'viewReview' in request.POST:
        if request.POST.get('req_id', False):

            req_id = request.POST['req_id']
            req = Request_Paper_Review.objects.get(id=req_id)

            reviewer_id = req.reviewer.id
            document_id = req.document.id

            doc_reviews = Review.objects.filter(reviewer=user,document=req.document)

            paperSummary = ''
            reviewReasons = ''
            rating = ''

            for doc_Rev in doc_reviews:
                paperSummary = doc_Rev.paperSummary
                reviewReasons = doc_Rev.reviewReasons
                rating = doc_Rev.rating

            context = {
                'user':user,
                'paperSummary':paperSummary,
                'reviewReasons':reviewReasons,
                'rating':rating,
                'doc_title':req.document.doc_title,
                'doc_ID':document_id,
                'perm_can_review_doc': perm_can_review_doc,
                'perm_can_edit_rev_req': perm_can_edit_rev_req,
                'perm_can_submit_paper':perm_can_submit_paper
            }
            return render_to_response(
                'pcm_views/viewReview.html',
                context_instance = RequestContext(
                    request, context
                )
            )

    elif request.method == 'POST' and 'editReview' in request.POST:
        if request.POST.get('req_id', False):

            req_id = request.POST['req_id']
            req = Request_Paper_Review.objects.get(id=req_id)

            reviewer_id = req.reviewer.id
            document_id = req.document.id

            doc_reviews = Review.objects.filter(reviewer=user,document=req.document)

            doc_review=''

            for doc_Rev in doc_reviews:
                doc_review=doc_Rev

            print(doc_review.paperSummary)
            print(doc_review.reviewReasons)
            print(doc_review.rating)

            form = ReviewRatingForm()
            form.fields['doc_id'].initial = document_id
            form.fields['paper_summary'].initial = doc_review.paperSummary
            form.fields['review'].initial = doc_review.reviewReasons
            form.fields['rating'].initial = doc_review.rating

            context = {
                'user':user,
                'form':form,
                'document_title':req.document.doc_title,
                'perm_can_review_doc': perm_can_review_doc,
                'perm_can_edit_rev_req': perm_can_edit_rev_req,
                'perm_can_submit_paper':perm_can_submit_paper
            }
            return render_to_response(
                'pcm_views/editReview.html',
                context_instance = RequestContext(
                    request, context
                )
            )

    elif request.method == 'POST' and 'addReview' in request.POST:
        if request.POST.get('req_id', False):

            req_id = request.POST['req_id']
            req = Request_Paper_Review.objects.get(id=req_id)

            reviewer_id = req.reviewer.id
            document_title = req.document.doc_title
            print(req.document.id)

            form = ReviewRatingForm()
            form.fields['doc_id'].initial = req.document.id

            context = {
                'user':user,
                'document_title':document_title,
                'form':form,
                'perm_can_review_doc': perm_can_review_doc,
                'perm_can_edit_rev_req': perm_can_edit_rev_req,
                'perm_can_submit_paper':perm_can_submit_paper
            }
            return render_to_response(
                'pcm_views/addReview.html',
                context_instance = RequestContext(
                    request, context
                )
            )

    else:

        return render_to_response(
            'pcm_views/viewAssignedPapers.html',
            context_instance = RequestContext(
                request, context
            )
        )


# To add review and rating for documents only allowed for PCMs and PCC.
@login_required
def addReview(request):

    perm_can_review_doc = False
    perm_can_edit_rev_req = False
    perm_can_submit_paper  = False

    if request.user.has_perm("firstApp.add_documentsubmission"):
        perm_can_submit_paper = True


    if request.user.has_perm("firstApp.add_review") and request.user.has_perm("firstApp.change_review"):
        perm_can_review_doc = True
    if request.user.has_perm("firstApp.change_request_paper_review"):
        perm_can_edit_rev_req = True

    user = request.user
    if request.method == 'POST':
        print('add review')
        print(request.POST)
        form = ReviewRatingForm(request.POST)
        if form.is_valid():
            print('add review form')

            doc = DocumentSubmission.objects.get(id=form.cleaned_data['doc_id'])
            rev = user

            review = Review(
                document=doc,
                reviewer=rev,
                paperSummary=form.cleaned_data['paper_summary'],
                rating=form.cleaned_data['rating'],
                reviewReasons=form.cleaned_data['review']
            )

            review.save()
            context = {
                'perm_can_review_doc': perm_can_review_doc,
                'perm_can_edit_rev_req': perm_can_edit_rev_req,
                'perm_can_submit_paper':perm_can_submit_paper
            }
            return render_to_response(
                'pcm_views/add_review_success.html',
                context_instance = RequestContext(
                    request,context
                )
            )

# To update review and rating for documents only allowed for PCMs and PCC.
@login_required
def updateReview(request):

    perm_can_review_doc = False
    perm_can_edit_rev_req = False

    perm_can_submit_paper  = False

    if request.user.has_perm("firstApp.add_documentsubmission"):
        perm_can_submit_paper = True


    if request.user.has_perm("firstApp.add_review") and request.user.has_perm("firstApp.change_review"):
        perm_can_review_doc = True
    if request.user.has_perm("firstApp.change_request_paper_review"):
        perm_can_edit_rev_req = True

    user = request.user
    if request.method == 'POST':
        print('edit review')
        print(request.POST)
        form = ReviewRatingForm(request.POST)
        if form.is_valid():
            print('edit review form')

            doc = DocumentSubmission.objects.get(id=form.cleaned_data['doc_id'])
            rev = user

            doc_reviews = Review.objects.filter(reviewer=rev,document=doc)

            doc_review=''

            for doc_Rev in doc_reviews:
                doc_review=doc_Rev

            doc_review.paperSummary=form.cleaned_data['paper_summary']
            doc_review.reviewReasons=form.cleaned_data['review']
            doc_review.rating=form.cleaned_data['rating']

            doc_review.save()

            context = {
                'perm_can_review_doc': perm_can_review_doc,
                'perm_can_edit_rev_req': perm_can_edit_rev_req,
                'perm_can_submit_paper':perm_can_submit_paper
            }

            return render_to_response(
                'pcm_views/edit_Review_success.html',
                context_instance = RequestContext(
                    request,context
                )
            )

# To assign documents for review. only allowed for PCC.
@login_required
def assignPapersToReview(request):

    perm_can_review_doc = False
    perm_can_edit_rev_req = False

    perm_can_submit_paper  = False
    isWithinDeadline = False
    assignpaperDeadlines = Deadline.objects.filter(type='Assign Paper')
    if assignpaperDeadlines.count() > 0:
        psDeadline = assignpaperDeadlines[0]
        currentDate = datetime.date.today()
        isWithinDeadline = currentDate >= psDeadline.from_date and currentDate <= psDeadline.to_date

    if request.user.has_perm("firstApp.add_documentsubmission"):
        perm_can_submit_paper = True

    users=[]
    pcms=[]
    docs_unassigned=[]
    docs_unassigned_ids=[]
    dict_count={}

    if request.user.has_perm("firstApp.add_review") and request.user.has_perm("firstApp.change_review"):
        perm_can_review_doc = True
    if request.user.has_perm("firstApp.change_request_paper_review"):
        perm_can_edit_rev_req = True

    user = request.user
    all_doc_submissions = DocumentSubmission.objects.all()
    doc_sub_ids=[]
    rev_req_approved = Request_Paper_Review.objects.filter(status='Approved')
    
    print('rev_req_approved')
    print(rev_req_approved)

    for doc in all_doc_submissions:
        doc_sub_ids.append(doc.id)

    for doc_id in doc_sub_ids:
        reviewer_count=0
        for rev_doc in rev_req_approved:
            if doc_id == rev_doc.document_id:
                reviewer_count=reviewer_count+1
        if reviewer_count != 3:
            docs_unassigned_ids.append(doc_id)
            doc = DocumentSubmission.objects.get(id=doc_id)
            dict_count[doc]= 3 - reviewer_count

    print('docs_unassigned_ids')
    print(docs_unassigned_ids)

    docs_unassigned=DocumentSubmission.objects.filter(pk__in=docs_unassigned_ids)
    print(docs_unassigned)

    if request.method == 'POST' and 'previewDoc' in request.POST:
        print('POST')
        if request.POST.get('document', False):
            doc_id = request.POST['document']
            print(doc_id)
            doc = DocumentSubmission.objects.get(id=doc_id)
            doc_name = doc.document.name
            doc_format = doc.doc_format

            context = {
                'user':user,
                'doc':doc,
                'doc_name':doc_name,
                'doc_format':doc_format,
                'perm_can_review_doc': perm_can_review_doc,
                'perm_can_edit_rev_req': perm_can_edit_rev_req,
                'perm_can_submit_paper':perm_can_submit_paper,
                'is_within_deadline': isWithinDeadline
            }

        if 'PDF' == doc_format:
            image_data = open(MEDIA_ROOT+'/'+doc_name, 'rb').read()
            return HttpResponse(image_data, content_type='application/pdf')
        else:
            image_data = open(MEDIA_ROOT+'/'+doc_name, 'rb').read()
            return HttpResponse(image_data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')


    elif request.method == 'POST' and 'assignPaper' in request.POST:

        users=User.objects.all()
        for usr in users:
            if usr.has_perm("firstApp.add_review"):
                pcms.append(usr)

        form = request.POST
        selected_reviewers = request.POST.getlist('pcm_id')
        print(selected_reviewers)
        doc_id = request.POST['document']
        print(doc_id)
        doc = DocumentSubmission.objects.get(id=doc_id)
        doc_name = doc.document.name
        doc_format = doc.doc_format
        for pcm_id in selected_reviewers:
            user = User.objects.get(id=pcm_id)
            print(user)
            request_Paper_Review = Request_Paper_Review(
                document=doc,
                reviewer=user,
                status='Approved'
                )

            request_Paper_Review.save()
            return HttpResponseRedirect('/assignPapersToReview/')

    else:
        users=User.objects.all()
        for usr in users:
            if usr.has_perm("firstApp.add_review"):
                pcms.append(usr)

    context = {
                'perm_can_review_doc': perm_can_review_doc,
                'perm_can_edit_rev_req': perm_can_edit_rev_req,
                'pcms':pcms,
                'all_doc_submissions':all_doc_submissions,
                'docs_unassigned':docs_unassigned,
                'dict_count':dict_count,
                'perm_can_submit_paper':perm_can_submit_paper,
                'is_within_deadline': isWithinDeadline,
            }
    return render_to_response(
                'pcc_views/assignPapersToReview.html',
                context_instance = RequestContext(
                    request,context
                )
            )


@login_required
def templates(request):
    perm_can_review_doc = False
    perm_can_edit_rev_req = False
    if request.user.has_perm("firstApp.add_review") and request.user.has_perm("firstApp.change_review"):
        perm_can_review_doc = True
    if request.user.has_perm("firstApp.change_request_paper_review"):
        perm_can_edit_rev_req = True

    # Create the formset, specifying the form and formset we want to use.
    TemplateFormSet = modelformset_factory(
        Template,
        fields=(
            'template_type',
            'message'
        ),
        widgets={
            'template_type': Select(),
            'message': Textarea()
        },
        can_delete=True
    )

    if request.method == 'POST':
        template_formset = TemplateFormSet(request.POST)
        if template_formset.is_valid():
            template_formset.save()
            return HttpResponseRedirect('/templates/')
    else:
        templateQuerySet = Template.objects.all()
        template_formset = TemplateFormSet(queryset=templateQuerySet)

    context = {
        'perm_can_review_doc': perm_can_review_doc,
        'perm_can_edit_rev_req': perm_can_edit_rev_req,
        'template_formset': template_formset
    }

    return render_to_response(
        'admin_views/templates.html',
        context_instance = RequestContext(
            request,
            context
        )
    )


@login_required
def deadlines(request):
    perm_can_review_doc = False
    perm_can_edit_rev_req = False
    if request.user.has_perm("firstApp.add_review") and request.user.has_perm("firstApp.change_review"):
        perm_can_review_doc = True
    if request.user.has_perm("firstApp.change_request_paper_review"):
        perm_can_edit_rev_req = True

    # Create the formset, specifying the form and formset we want to use.
    DeadlineFormSet = modelformset_factory(
        Deadline,
        fields=(
            'type',
            'from_date',
            'to_date'
        ),
        widgets={
            'type': Select(),
            'from_date': DateInput(),
            'to_date': DateInput()
        },
        can_delete=True
    )

    if request.method == 'POST':
        deadline_formset = DeadlineFormSet(request.POST)
        if deadline_formset.is_valid():
            deadline_formset.save()
            return HttpResponseRedirect('/deadlines/')
    else:
        deadlineQuerySet = Deadline.objects.all()
        deadline_formset = DeadlineFormSet(queryset=deadlineQuerySet)

    context = {
        'perm_can_review_doc': perm_can_review_doc,
        'perm_can_edit_rev_req': perm_can_edit_rev_req,
        'deadline_formset': deadline_formset
    }

    return render_to_response(
        'admin_views/deadlines.html',
        context_instance = RequestContext(
            request,
            context
        )
    )


# To view all 3 reviews for document and provide final rating or generate notification in case of conflict.
@login_required
def provideFinalRating(request):

    perm_can_review_doc = False
    perm_can_edit_rev_req = False
    perm_can_submit_paper  = False
    isWithinDeadline = False
    finalreviewDeadlines = Deadline.objects.filter(type='Final Review')
    if finalreviewDeadlines.count() > 0:
        psDeadline = finalreviewDeadlines[0]
        currentDate = datetime.date.today()
        isWithinDeadline = currentDate >= psDeadline.from_date and currentDate <= psDeadline.to_date

    if request.user.has_perm("firstApp.add_documentsubmission"):
        perm_can_submit_paper = True

    if request.user.has_perm("firstApp.add_review") and request.user.has_perm("firstApp.change_review"):
        perm_can_review_doc = True

    if request.user.has_perm("firstApp.change_request_paper_review"):
        perm_can_edit_rev_req = True

    rating_choices = [1,2,3,4,5]

    doc_reviews = Review.objects.all()
    #doc_reviews_1 = Review.objects.filter(reviewer=rev,document=doc)
    doc_tot_rev={}
    doc_rev_list=[]

    all_docs = DocumentSubmission.objects.all()

    for doc in all_docs:
        doc_tot_rev[doc]=[]

    for doc_rev in doc_reviews:
        if doc_rev.document in doc_tot_rev:
            doc_all_reviews = Review.objects.all().filter(document=doc_rev.document)
            doc_tot_rev[doc_rev.document] = doc_all_reviews

    context = {
                'user':request.user,
                'perm_can_review_doc': perm_can_review_doc,
                'perm_can_edit_rev_req': perm_can_edit_rev_req,
                'perm_can_submit_paper':perm_can_submit_paper,
                'doc_tot_rev':doc_tot_rev,
                'rating_choices':rating_choices,
                'is_within_deadline': isWithinDeadline
            }

    if request.method == 'POST' and 'saveRating' in request.POST:
        form = request.POST
        final_rating = request.POST.get('rate_id')
        doc_id = request.POST['document_id']
        print(doc_id)
        doc = DocumentSubmission.objects.get(id=doc_id)
        doc.finalRating=final_rating
        doc.status='Reviewed'
        doc.save()
        return HttpResponseRedirect('/provideFinalRating/')

    elif request.method == 'POST' and 'reportConflict' in request.POST:
        print('report conflict')
        form = request.POST
        print(request.POST['document_id'])
        doc_id = request.POST['document_id']
        print(doc_id)

        # fetch document
        document = DocumentSubmission.objects.get(id=doc_id)
        # fetch reviwers objects.
        reviewer_ids = Review.objects.values('reviewer').filter(document=document)

        reviewers = User.objects.filter(pk__in=reviewer_ids)
        
        for rev in reviewers:
            print(rev.first_name)

        # send notification to reviewers
        signals.report_conflict_signal.send(
                    sender=None,
                    pcm_reviewers=reviewers,
                    doc_submission=document
                )

    return render_to_response(
                'pcc_views/provideFinalRating.html',
                context_instance = RequestContext(
                    request,context
                )
            )

