# -*- coding: utf-8 -*-
import os


from django.conf.urls import url
from django.contrib.auth.views import logout

from .views import (
	Login, Signup,ResetPassword,ChangePassword,Profile,logoutuser,UpdateProfile,BookShop,BookDetails,
)

urlpatterns = [
    url(r'^$', Login.as_view(), name='login'),
    url(r'^signup/$', Signup.as_view(), name='signup'),
    url(r'^reset_password/$', ResetPassword.as_view(),name="reset_password"),
    url(r'^change_password/$',ChangePassword.as_view(),name="change_password"),
    url(r'^profile/$',Profile.as_view(),name="profile"),
    url(r'^update_profiles/$',UpdateProfile.as_view(),name="update_profile"),
    url(r'^logout/$',logoutuser,name="logout"),
    url(r'^book_shop/$',BookShop.as_view(),name="book_shop"),
    url(r'^shop/(?P<slug>[\w-]+)/book_detail/$', BookDetails.as_view(), name='show_book'),
]	