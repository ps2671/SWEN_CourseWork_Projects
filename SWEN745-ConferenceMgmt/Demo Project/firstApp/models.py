from django.db import models
from django.contrib.auth.models import User

# Tuple definitions.
doc_format_choices = (
    ('PDF', 'PDF'),
    ('Word Document', 'Word Document')
)
event_type_choices = (
    ('PAPER_SUBMISSION', 'Paper Submission'),
    ('ACCOUNT_UPDATE', 'Account Update'),
    ('PCM_ACCOUNT_DELETION', 'PCM Account Deletion'),
    ('PCM_ASSIGNED_PAPER', 'PCM Assigned Paper'),
    ('REVIEWS_COMPLETE', 'Reviews Complete'),
    ('PAPER_SUBMISSION_REMINDER', 'Paper Submission Reminder'),
    ('PCM_SUBMIT_REVIEW' , 'PCM Submit Review'),
    ('PCM_SUBMIT_REVIEW_LIST','PCM Submit Review List'),
    ('FINAL_RATING', 'Final Rating for submission is complete'),
    ('REVIEW_CONFLICT', 'Review Conflict')
)
deadline_type_choices = (
    ('Paper Submit', 'Paper submission by Author'),
    ('Review List', 'Review list of choices by PCM'),
    ('Assign Paper', 'Assign paper to PCM'),
    ('Submit Review','Submit review of papers by PCM'),
    ('Final Review', 'Submit final review by PCC')
)
rev_req_status_choices = (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected')
)
template_type_choices = (
    ('PAPER_SUBMISSION_AUTHOR_NOTIF', 'Paper Submission Notification for Author'),
    ('PAPER_SUBMISSION_PCC_NOTIF', 'Paper Submission Notification for PCC'),
    ('REVIEW_REQUEST_APPROVED_PCM_NOTIF', 'Review Request Approved Notification for PCM'),
    ('REVIEW_REQUEST_REJECTED_PCM_NOTIF', 'Review Request Rejected Notification for PCM'),
    ('REVIEWS_COMPLETE_PCC_NOTIF', 'Reviews Complete Notification for PCC'),
    ('USER_ACCOUNT_UPDATE_NOTIF', 'User Account Update Notification'),
    ('FINAL_RATING_AUTHOR_NOTIF', 'Final Rating Notification for Author')
)

# Create your models here.
class UserProfile(models.Model):
    # UserProfile model has a one-to-one reference to User Model.
    user = models.OneToOneField(User)
    affiliation = models.CharField(max_length=25,default='RIT')

    def __unicode__(self):
        return self.user.username

class DocumentSubmission(models.Model):
    # paper, list of authors, contact author, indication of whether the paper is a revision, and format of the paper.
    submitter = models.ForeignKey(User)
    doc_title = models.CharField(max_length=100)
    submitter_email = models.EmailField(max_length=70, blank=False, null=False, unique=False,default='sally@rit.edu')
    doc_version = models.IntegerField()
    doc_format = models.CharField(max_length=6, choices=doc_format_choices)
    status = models.CharField(max_length=500, blank=False, null=False, unique=False,default='Submitted')
    document = models.FileField(upload_to="sam_2017/docs/")
    finalRating = models.CharField(max_length=500, blank=True, null=True, unique=False)

    def __str__(self):
        return self.doc_title

class NotificationQuerySet(models.query.QuerySet):
    def unread(self):
        return self.filter(is_read=False)

class Notification(models.Model):
    # The Notification model has a many-to-one reference to the User Model.
    # A User can have multiple Notifications, some read or unread, while a
    # Notification refers to only one User.
    event_type = models.CharField(max_length=50, choices=event_type_choices)
    recipient = models.ForeignKey(User, blank=False, null=False, related_name='notifications')
    is_read = models.BooleanField(blank=False, null=False, unique=False, default=False)
    message = models.CharField(max_length=500, blank=False, null=False, unique=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    objects = NotificationQuerySet.as_manager()

    class Meta:
        ordering = ['-created_date']

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save()

class Deadline(models.Model):
    to_date = models.DateField(null=False)
    from_date = models.DateField(null=False)
    type = models.CharField(max_length=50, choices=deadline_type_choices, blank=False, null=False, unique=True)
    message = models.CharField(max_length=100, blank=False, null=False)

    def clean(self):
        if self.to_date < self.from_date:
            raise ValidationError('Start date is after end date')

class Deadline_User(models.Model):
    type=models.ForeignKey(Deadline,on_delete=models.CASCADE)
    receipient=models.ForeignKey(User)
    is_read=models.BooleanField(default='False')

class DocumentContributor(models.Model):
    document = models.ForeignKey(DocumentSubmission)
    contributor_name = models.CharField(max_length=100, blank=True, null=True, unique=False, default='sally')
    contributor_email = models.EmailField(max_length=70, blank=True, null=True, unique=False, default='sally@rit.edu')

    def __str__(self):
        return self.contributor_name

class Review(models.Model):
    document = models.ForeignKey(DocumentSubmission)
    reviewer = models.ForeignKey(User)
    paperSummary = models.CharField(max_length=500, blank=True, null=True, unique=False, default='paper')
    rating = models.CharField(max_length=500, blank=True, null=True, unique=False, default='1')
    reviewReasons = models.CharField(max_length=500, blank=True, null=True, unique=False, default='average')

    def __str__(self):
        return self.paperSummary

class Request_Paper_Review(models.Model):
    document = models.ForeignKey(DocumentSubmission)
    reviewer = models.ForeignKey(User)
    status = models.CharField(max_length=10,choices=rev_req_status_choices)

    def __str__(self):
        return self.status

class Template(models.Model):
    template_type = models.CharField(max_length=50, choices=template_type_choices, unique=True)
    message = models.CharField(max_length=500, blank=True, null=True, unique=False, default='Template message')