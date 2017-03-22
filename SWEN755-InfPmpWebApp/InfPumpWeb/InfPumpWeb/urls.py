from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'InfPumpWeb_app.views.login.user_login'),
    url(r'^accounts/login/$', 'InfPumpWeb_app.views.login1.user_login1'),

    url(r'^registration/$', 'InfPumpWeb_app.views.registration.user_registration', name='registration'),

    url(r'^user_profile/$', 'InfPumpWeb_app.views.user_profile.user_profile', name='profile'),

    url(r'^user_profile/logout/$', 'InfPumpWeb_app.views.logout.logout_page', name='logout'),

    url(r'^user_profile/user_information/$', 'InfPumpWeb_app.views.update_user_info.manage_account', name='modify_user_info'),
    url(r'^user_profile/prescription/$', 'InfPumpWeb_app.views.prescription.prescription', name='modify_user_info'),
    url(r'^user_profile/list/$', 'InfPumpWeb_app.views.list.list', name='modify_user_info'),
    url(r'^user_profile/patient_list/$', 'InfPumpWeb_app.views.patient_list.patient_list'),
    url(r'^user_profile/doctor_list/$', 'InfPumpWeb_app.views.doctor_list.doctor_list'),
 

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
