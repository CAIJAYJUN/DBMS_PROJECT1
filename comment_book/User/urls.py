from django import views
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from User import views
urlpatterns = [
<<<<<<< HEAD
url(r'^register/$',views.register),
url(r'^login/$',views.login),
url(r"^main/$", views.main),
url(r"^build_bookshelf/$", views.build_bookshelf),
url(r'^registerAdmin/$',views.register_admin),
url(r'^admin_login/$',views.adminLogin),
url(r'^main_manage/$',views.mainManage),
url(r'^logout/$',views.logout),
url(r'^admin_logout/$',views.adminLogout),


]
=======
    url(r"^register/$", views.register),
    url(r"^login/$", views.login),
    url(r"^main/$", views.main),  # 登入後頁面
    url(r"^build_bookshelf/$", views.build_bookshelf, name="build_bookshelf"),  # 建立書架
    url(r"^user_comment/$", views.user_comment, name="user_comment"),  # 建立書架
    url(r"^registerAdmin/$", views.register_admin),
    url(r"^admin_login/$", views.adminLogin),
    url(r"^main_manage/$", views.mainManage),
    url(r"^logout/$", views.logout),
    url(r"^admin_logout/$", views.adminLogout),
]
>>>>>>> 13e3f7b (add user comment)
