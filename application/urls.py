"""transsport_project URL Configuration

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
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.conf.urls import include
from .utils import PlaceResource

from . import views

place_resource = PlaceResource()

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('account/', views.account, name='account'),
    re_path(r'^search/$', views.search_places, name='search'),
    path('create-account/', views.create_account.as_view(), name='create_account'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    path('modify-account/', views.modify_account, name='modify_account'),
    path('suggesting-new-place/', views.suggesting_new_place, name='suggesting_new_place'),
    path('all-places/', views.all_places, name='all_places'),
    path('all-departments/', views.all_departments, name='all_departments'),
    re_path(r'^all-departments/(?P<postal_code>[0-9]+)/$', views.places_by_departments, name='places_by_departments'),
    re_path(r'^all-places/(?P<place_id>[0-9]+)/$', views.show_place, name='show_place'),
    re_path(r'^all-places/(?P<place_id>[0-9]+)/edit-comment/', views.edit_comment, name='edit_comment'),
    re_path(r'^all-places/(?P<place_id>[0-9]+)/make-comment/', views.make_comment, name='make_comment'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='application/registration/password_reset_form.html'), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='application/registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='application/registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='application/registration/password_reset_complete.html'), name='password_reset_complete'),
    path('api/', include(place_resource.urls)),
]
