"""Demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, patterns, include
from django.contrib import admin
from django.contrib.auth import views
from firstApp.views import *

urlpatterns = [
    url(r'^$', views.login), # If user is not login it will redirect to login page
    url(r'^logout/$', logout_page),
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    url(r'^home/$', home),
    url(r'^myProfile/$', myProfile),
    url(r'^submitDoc/$', docSubmission),
    url(r'^updateProfile/$', updateProfile),
    url(r'^viewSubmission/$', viewSubmission),
    url(r'^viewPDF/(?P<id>\d+)/$', viewPDF, name='viewPDF'),
    url(r'^viewAllSubmissions/$', viewAllSubmissions),
    url(r'^viewReviewRequests/$', viewReviewRequests),
    url(r'^requestPaperToReview/$', requestPaperToReview),
    url(r'^viewRevReqStatus/$', viewRevReqStatus),
    url(r'^viewAssignedPapers/$', viewAssignedPapers),
    url(r'^provideFinalRating/$', provideFinalRating),
    url(r'^addReview/$', addReview),
    url(r'^updateReview/$', updateReview),
    url(r'^assignPapersToReview/$', assignPapersToReview),
    url(r'^admin/', admin.site.urls),
    url(r'^templates/', templates),
    url(r'^deadlines/', deadlines),
    url(r'^mark-as-read/(?P<id>\d+)/$', mark_as_read, name='mark_as_read'),
    url(r'^api/unread_count/$', live_unread_notification_count, name='live_unread_notification_count'),
    url(r'^api/all_list/$', live_all_notification_list, name='live_all_notification_list'),
]
