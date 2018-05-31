from django.conf.urls import include, url
from . import views


urlpatterns = [
#    url(r'^post/(?P<pk>[0-9]+)/$',views.post_detail,name='post'),
#        url(r'^$', views.post_list,name='index'),
#        url(r'^post/new/$', views.post_ack, name='post_ack'),
#        url(r'^post/edit/(?P<pk>[0-9]+)/$', views.post_edit, name='post_edit'),
#        url(r'^signup/$',views.signup_view,name='signup'),
#        url(r'^login/$',views.login_view,name='login'),
#        url(r'^logout/$',views.logout_view,name='logout'),
#        url(r'^search/$',views.ajax,name='search'),
       url(r'^index0/$',views.index0,name='index0'),

]
