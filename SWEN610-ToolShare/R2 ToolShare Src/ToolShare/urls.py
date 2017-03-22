"""ToolShare URL Configuration

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
from firstApp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/',admin.site.urls),
    url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'), # If user is not login it will redirect to login page
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    url(r'^home/$', home),
    url(r'^myProfile/$', myProfile),
    url(r'^viewTool/$', viewTool),
    url(r'^showAllRecentTools/$', showAllRecentTools),
    url(r'^showAllHighRatedTools/$', showAllHighRatedTools),
    url(r'^showAllMostActiveUsers/$', showAllMostActiveUsers),
    url(r'^changePassword/$', changePassword),
    url(r'^changePasswordSuccess/$', changePasswordSuccess),
    url(r'^myTools/$', myTools),
    url(r'^myTools/requestedTool/$', viewRequests),
    url(r'^myTools/myRequests/$', myRequests),
    url(r'^myTools/otherAcceptedRequest/$', otherAcceptedRequests),
    url(r'^addNewTool/$', myToolsRegistration),
    url(r'^manageMyTools/$', myRegisteredTools),
    url(r'^borrowTools/$', borrowTool),
    url(r'^toolUpdate/$', myToolUpdate),
    url(r'^myTools/returnTools/$', returnTools),
    url(r'^tools/register/success/$', myToolsRegistration),
    url(r'^ShareZone/$', ShareZoneView),
    url(r'^ShareZoneUsers/$', ShareZoneUsersView),
    url(r'^cshed/$', CreateCommunityShed),
    url(r'^ManageUsers/$', ManageUsers),
    url(r'^(?P<user_id>[0-9]+)/UpdateUser/$', UpdateUser, name='UpdateUser'),
    url(r'^ManageTools/$', ManageTools),
    url(r'^(?P<tool_id>[0-9]+)/UpdateTool/$', UpdateTool, name='UpdateTool'),
    url(r'^UsersPermission/$', noPermission),
    url(r'^ToolsPermission/$', noPermission_tool),
    url(r'^ManageUsersAdmin/$', ManageUsersAdmin),
    url(r'^(?P<user_id>[0-9]+)/UpdateUserAdmin/$', UpdateUserAdmin, name='UpdateUserAdmin'),
    url(r'^ManageToolsAdmin/$', ManageToolsAdmin),
    url(r'^(?P<tool_id>[0-9]+)/UpdateToolAdmin/$', UpdateToolAdmin, name='UpdateToolAdmin'),
    url(r'^ManageSharezone/$', ManageSharezone),
    url(r'^(?P<shz_id>[0-9]+)/UpdateShed/$', UpdateShed, name='UpdateShed'),
    url(r'^CannotRemoveUser/$', CannotRemoveUser),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
