from django import views
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from User import views
urlpatterns = [
    url(r'^register/$',views.register),
    url(r'^login/$',views.login),
    url(r"^main/$", views.main),
    # url(r"^build_bookshelf/$", views.build_bookshelf),
    url(r'^registerAdmin/$',views.register_admin),
    url(r'^admin_login/$',views.adminLogin),
    url(r'^main_manage/$',views.mainManage),
    url(r'^logout/$',views.logout),
    url(r'^admin_logout/$',views.adminLogout),
    path('comment/<str:isbn>',views.user_comment,name="comment"),
    path('build_bookshelf/<str:isbn>',views.build_bookshelf,name="build_bookshelf"),
    url(r'^searchBook/$',views.searchBook,name="searchBook"),
    url(r'^getUserList/$',views.listUserBook)



    # url(r'^searchResult/$',views.searchResult,name="searchResult"),

    # url(r"^user_comment/$", views.user_comment, name="user_comment"),
]