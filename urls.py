from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^repomanager/', include('repomanager.foo.urls')),
    (r'^$', 'repomanager.repos.views.frontpage'),

    # repos
    (r'^repos/$', 'repomanager.repos.views.frontpage'),
    (r'^repos/adduser/$', 'repomanager.repos.views.adduser'),
    (r'^repos/deluser/$', 'repomanager.repos.views.deluser'),
    (r'^repos/create/$', 'repomanager.repos.views.create'),
    (r'^repos/delete/$', 'repomanager.repos.views.delete'),
    # accounts
    (r'^accounts/$', 'repomanager.accountsviews.frontpage'),
    (r'^accounts/profile/$', 'repomanager.accountsviews.profile'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^accounts/change_password/$','django.contrib.auth.views.password_change'),
    (r'^accounts/change_password/done/$','django.contrib.auth.views.password_change_done'),

    # Uncomment the next line to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line for to enable the admin:
    (r'^admin/(.*)', admin.site.root),

    (r'^tos/', direct_to_template, {'template':'tos.html'}),
    (r'^about/', direct_to_template, {'template':'about.html'}),

)
