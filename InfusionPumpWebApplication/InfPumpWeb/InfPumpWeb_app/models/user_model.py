from django.db import models
from django.contrib.auth.models import User

# # This is a user class
# class User(models.Model):

#     DOCTOR = "Doctor"
#     PATIENT = "Patient"
#     ADMIN = "Admin"

#     USER_TYPE = ((DOCTOR, "Doctor"), (PATIENT, "Patient"), (ADMIN, "Admin"))

#     first_name = models.CharField(max_length=30, blank=False)
#     last_name = models.CharField(max_length=30, blank=False)
#     email = models.EmailField()
#     password = models.CharField(max_length=50)
#     type = models.CharField(max_length=10, choices=USER_TYPE, default=DOCTOR)
#     admin = models.BooleanField(default=False)

#     class Meta:
#         app_label = 'InfPumpWeb_app'

#     def __str__(self):
#         return self.email

class UserProfile (models.Model):

    DOCTOR = "Doctor"
    PATIENT = "Patient"
    ADMIN = "Admin"

    USER_TYPE = ((DOCTOR, "Doctor"), (PATIENT, "Patient"), (ADMIN, "Admin"))

    # UserProfile model extends User Model.
    user = models.OneToOneField(User)
    type = models.CharField(max_length=10, choices=USER_TYPE, default=PATIENT)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
         return self.type
