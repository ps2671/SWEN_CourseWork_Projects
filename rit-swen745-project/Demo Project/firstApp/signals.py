from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from firstApp.models import *


# Generate notifications when an author submits a paper
@receiver(post_save, sender=DocumentSubmission)
def document_submitted(sender, **kwargs):
    docSubmission = kwargs['instance']
    if (docSubmission is not None
            and docSubmission.doc_title is not None
            and docSubmission.doc_version is not None
            and docSubmission.submitter is not None):
        if docSubmission.status=='Reviewed':
            submitter = docSubmission.submitter
            templ = Template.objects.get(template_type='FINAL_RATING_AUTHOR_NOTIF')
            authorNotification = Notification(event_type='FINAL_RATING', recipient=submitter, message=templ.message)
            authorNotification.save()

        elif docSubmission.status=='Submitted':
            submitter = docSubmission.submitter
            templ = Template.objects.get(template_type='PAPER_SUBMISSION_AUTHOR_NOTIF')
            authorNotification = Notification(event_type='PAPER_SUBMISSION', recipient=submitter, message=templ.message)
            authorNotification.save()

            # Note: Need to get the only 1 PCC user for workshop
            pccUsers = User.objects.filter(groups__name='PCC')
            if len(pccUsers) >= 1:
                pccUser = pccUsers[0]
                templ = Template.objects.get(template_type='PAPER_SUBMISSION_PCC_NOTIF')
                pccNotification = Notification(event_type='PAPER_SUBMISSION', recipient=pccUser, message=templ.message)
                pccNotification.save()


# Generate a notification when a PCC updates a paper review request
@receiver(post_save, sender=Request_Paper_Review)
def request_paper_review_submitted(sender, **kwargs):
    paperReviewRequest = kwargs['instance']
    if (paperReviewRequest is not None
            and paperReviewRequest.reviewer is not None
            and paperReviewRequest.document is not None
            and paperReviewRequest.status is not None):
        if paperReviewRequest.status == 'Approved':
            pcmReviewer = paperReviewRequest.reviewer
            templ = Template.objects.get(template_type='REVIEW_REQUEST_APPROVED_PCM_NOTIF')
            pcmNotification = Notification(event_type='PCM_ASSIGNED_PAPER', recipient=pcmReviewer, message=templ.message)
            pcmNotification.save()
        elif paperReviewRequest.status == 'Rejected':
            pcmReviewer = paperReviewRequest.reviewer
            templ = Template.objects.get(template_type='REVIEW_REQUEST_REJECTED_PCM_NOTIF')
            pcmNotification = Notification(event_type='PCM_ASSIGNED_PAPER', recipient=pcmReviewer, message=templ.message)
            pcmNotification.save()


# Generate a notification when all reviews for a paper have been submitted
@receiver(post_save, sender=Review)
def review_submitted(sender, **kwargs):
    paperReview = kwargs['instance']
    if (paperReview is not None
            and paperReview.document is not None
            and paperReview.reviewer is not None
            and paperReview.paperSummary is not None
            and paperReview.rating is not None
            and paperReview.reviewReasons is not None):
        docReviews = Review.objects.filter(document=paperReview.document)
        if (docReviews.count() == 3):
            # Note: Need to get the only 1 PCC user for workshop
            pccUsers = User.objects.filter(groups__name='PCC')
            if len(pccUsers) >= 1:
                pccUser = pccUsers[0]
                templ = Template.objects.get(template_type='REVIEWS_COMPLETE_PCC_NOTIF')
                pccNotification = Notification(event_type='REVIEWS_COMPLETE', recipient=pccUser, message=templ.message)
                pccNotification.save()


# Generate a notification only if a User or UserProfile field was updated
def user_account_updated(sender, **kwargs):
    user_object = kwargs.get('user_object', None)
    updated_field_value_dict = kwargs.get('updated_field_value_dict', None)
    if (user_object is not None
            and updated_field_value_dict is not None
            and len(updated_field_value_dict) > 0):
        templ = Template.objects.get(template_type='USER_ACCOUNT_UPDATE_NOTIF')
        userNotification = Notification(event_type='ACCOUNT_UPDATE', recipient=user_object, message=templ.message)
        userNotification.save()

# Generate a notification only if a User or UserProfile field was updated
def report_conflict(sender, **kwargs):
    pcm_reviewers = kwargs.get('pcm_reviewers', None)
    doc_submission = kwargs.get('doc_submission', None)
    if (pcm_reviewers is not None
            and doc_submission is not None
            and len(pcm_reviewers) == 3):
        for pcm_review in pcm_reviewers:
            pcmMessage = 'Hello {0}, their is a review conflict for paper {1}. Please update your review.'.format(pcm_review.first_name,doc_submission.doc_title)
            pcmNotification = Notification(event_type='REVIEW_CONFLICT', recipient=pcm_review, message=pcmMessage)
            pcmNotification.save()

# NOTE: Custom signals must be defined at the bottom of this file; otherwise,
# their callback receivers won't be registered in the system

# Custom signal when a user account is updated
user_account_update_signal = Signal(providing_args=["user_object", "updated_field_value_dict"])
user_account_update_signal.connect(user_account_updated)

# Custom signal when a conflict in rating is reported.
report_conflict_signal = Signal(providing_args=["pcm_reviewers", "doc_submission"])
report_conflict_signal.connect(report_conflict)