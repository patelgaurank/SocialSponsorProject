"""SatsangApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib import auth
from django.urls import path, include, re_path, reverse
from django.views.generic.base import TemplateView
#from Pages.views import home_View
#from Log_App.views import lgin_view
from django.contrib.auth import views as lgin_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.conf.urls import include, url
from sponsorApp.views import *
from imsApp.views import *

print(auth_views)
urlpatterns = [
    url(r'^admin/', admin.site.urls),
	path('', lgin_view.LoginView.as_view(), {'template_name':"registration/login.html"}),
    #path('login/', lgin_view.LoginView.as_view(), {'template_name':"registration/login.html"}),
    #path('logout/', lgin_view.LogoutView.as_view(),{'template_name':"registration/logged_out.html"}),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    # url(r'^accounts/reset_password/', auth_views.PasswordResetView.as_view(template_name = "password_reset.html"), name ='reset_password'),
    # url(r'^accounts/reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "password_reset_sent.html"), name ='password_reset_done'),
    # url(r'^accounts/reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "password_reset_form.html"), name ='password_reset_confirm'),
    # url(r'^accounts/reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "password_reset_done.html"), name ='password_reset_complete'),

    url(r'^sponsor/dashboard/$', dashboard_view, name="Sponsor_Dashboard."),
    url(r'^sponsor/sponsordata/$', sponsorView, name="Sponsor_data"),
    url(r'^sponsor/sponsorform/$', sponsor_form_view, name="Sponsor_Form"),
    url(r'^sponsor/display/$', display_view, name="Display_Slide"),
    url(r'^sponsor/team/$', team_group_view, name="Team"),
    url(r'^sponsor/announcer/$', announcer_view, name="Announce_ Slide"),
    url(r'^sponsor/purposecode/$', purposecode_view, name="Purpose_Code"),
    url(r'^ims/imsdata/$', ims_data_table_view, name="IMS_data"),
    url(r'^ims/imsform/$', ims_form_view, name="IMS_form"),
    # Custom app url
    url(r'session_security/', include('session_security.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)