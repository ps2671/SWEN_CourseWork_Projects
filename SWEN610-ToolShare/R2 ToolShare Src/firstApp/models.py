from django.db import models
from django.forms import extras
from django.contrib.auth.models import User, Group, Permission
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class ShareZone(models.Model):
    zipCode = models.CharField(max_length=5, unique=True)
    has_CommunityShed = models.NullBooleanField(default=False)
    CommunityShedLocation = models.CharField(max_length=100, null=True)


    @classmethod
    def create(cls, zipCode):
        sharezone = cls(zipCode=zipCode)
        sharezone.save()
        return sharezone;

    def __str__(self):
        return str(self.pk)

class UserProfile (models.Model):

    # UserProfile model extends User Model.
    user = models.OneToOneField(User)
    address = models.CharField(max_length=100)
    zipCode = models.CharField(max_length=5)
    first_Name = models.CharField(max_length=25)
    last_Name = models.CharField(max_length=25)
    #notificationFrequency = models.CharField(max_length=25)
    pickupArrangements = models.CharField(max_length=25)
    date = models.DateField()
    ShareZone = models.ForeignKey(ShareZone, null=True)
    is_admin = models.NullBooleanField(default=False)
    request = models.NullBooleanField(default=False)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return str(self.first_Name) + ' ' + str(self.last_Name)


class ToolsRegister(models.Model):
    conditionChoices = (
        ('Good', 'Good'),
        ('Bad', 'Bad'),
        ('Ok', 'ok'),
    )
    categoryChoices = (
        ('Axe', 'Axe'),
        ('Hammer', 'Hammer'),
        ('Screw', 'Screw'),
        ('Shovel', 'Shovel'),
    )
    statusChoices = (
        ('Available', 'Available'),
        ('UnAvailable', 'UnAvailable'),
    )
    userProfile = models.ForeignKey(UserProfile)
    nameOfTheTool = models.CharField(max_length=100)
    addressOfTheTool = models.CharField(max_length=100)
    statusOfTheTool = models.CharField(default="Available", max_length=11)#Available or Unavailable
    categoryOfTheTool = models.CharField(max_length=6, choices=categoryChoices)
    conditionOfTheTool = models.CharField(max_length=4, choices=conditionChoices)
    image = models.FileField(blank=True, null=True)
    toolDescription = models.CharField(max_length=500);
    #this four should be removed from here and if they are used in any other functionalities, need to tranfer those functionalities as well e.g. notification
    requested = models.BooleanField(default=False)
    requester_id = models.CharField(default="0", max_length=100)
    borrowed = models.BooleanField(default=False)
    borrower_id = models.CharField(default="0", max_length=100)

    class Meta:
        ordering = ["-nameOfTheTool"]

    def __str__(self):
        return self.nameOfTheTool

class ToolAvailability(models.Model):
    toolId = models.ForeignKey(ToolsRegister)
    #availabileToDates = list of models.DateField
    #availabileFromDates = list of models.DateField


class ToolRequest(models.Model):
    toolId = models.ForeignKey(ToolsRegister)
    requester_id = models.CharField(max_length=100)
    requestedFromDate = models.DateField()
    requestedToDate = models.DateField()
    requestStatus = models.IntegerField() #0 for pending, 1 for approved/borrowed, 2 for rejected, 4 for returned

    def __str__(self):
        return self.toolId.nameOfTheTool

class ToolBorrowed(models.Model):
    toolId = models.ForeignKey(ToolsRegister)
    requestId = models.ForeignKey(ToolRequest)
    borrowerId = models.CharField(max_length=100)
    notified = models.BooleanField()

class ToolRejected(models.Model):
    toolId = models.ForeignKey(ToolsRegister)
    requestId = models.ForeignKey(ToolRequest)
    requesterId = models.CharField(max_length=100)
    rejectionReason = models.CharField(max_length=500)
    notified = models.BooleanField()

#From borrower perspective
class ToolReturn(models.Model):
    ratingChoices = (
        ('5', '5'),
        ('4', '4'),
        ('3', '3'),
        ('2', '2'),
        ('1', '1'),
    )
    toolId = models.ForeignKey(ToolsRegister)
    requestId = models.ForeignKey(ToolRequest)
    note = models.CharField(max_length=100,blank=False)#thank you note or any comment
    rating = models.CharField(max_length=6, choices=ratingChoices)

#From tool owner perspective
class ToolReturned(models.Model):
    ratingChoices = (
        ('Very Good', 'Very Good'),
        ('Good', 'Good'),
        ('Bad', 'Bad'),
        ('Worst', 'Worst'),
    )
    toolId = models.ForeignKey(ToolsRegister)
    requestId = models.ForeignKey(ToolRequest)
    requesterId = models.CharField(max_length=100)
    rating = models.CharField(max_length=6, choices=ratingChoices)