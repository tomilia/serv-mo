from django.conf.urls import include, url
from . import views

from importlib import import_module
from allauth.socialaccount import providers
from allauth.account.views import LogoutView,ConfirmEmailView,EmailVerificationSentView
from allauth.socialaccount.views import *

class LogoutView(LogoutView):
    template_name = 'allauth/account/logout.html'
class LoginCancelledView(LoginCancelledView):
    template_name = 'allauth/socialaccount/login_cancelled.html'
class LoginErrorView(LoginErrorView):
    template_name = 'allauth/socialaccount/authentication_error.html'
class SignupView(SignupView):
    template_name = 'allauth/socialaccount/signup.html'
class ConnectionsView(ConnectionsView):
    template_name = 'allauth/socialaccount/connections.html'
class ConfirmEmailView(ConfirmEmailView):
    template_name = 'allauth/account/email_confirm.html'
class EmailVerificationSentView(EmailVerificationSentView):
    template_name = 'allauth/account/verification_sent.html'
urlpatterns = [
#    url(r'^post/(?P<pk>[0-9]+)/$',views.post_detail,name='post'),
#        url(r'^$', views.post_list,name='index'),
#        url(r'^post/new/$', views.post_ack, name='post_ack'),
#        url(r'^post/edit/(?P<pk>[0-9]+)/$', views.post_edit, name='post_edit'),
        url(r'^signup/$',views.signup_view,name='signup'),
        url(r'^login/$',views.login_view,name='login'),
#        url(r'^search/$',views.ajax,name='search'),
        url(r'^index0/$',views.index0,name='index0'),
        url(r'^search0/$',views.search0,name='search0'),
        url(r'^search0/map/$',views.map,name='map'),
        url(r'^account_logout/$',views.logout_view,name='account_logout'),
        url(r'^profile0/$',views.profile,name='profile'),
        url(r'^filter/$',views.filter,name='filter'),
]
urlpatterns += [
    url(r'^accounts/login/cancelled/$', LoginCancelledView.as_view(),
        name='socialaccount_login_cancelled'),
    url(r'^accounts/login/error/$', LoginErrorView.as_view(),
        name='socialaccount_login_error'),
    url(r'^accounts/signup/$', SignupView.as_view(), name='socialaccount_signup'),
    url(r'^accounts/connections/$', ConnectionsView.as_view(), name='socialaccount_connections'),
]

for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + '.urls')
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, 'urlpatterns', None)
    if prov_urlpatterns:
        urlpatterns += prov_urlpatterns
