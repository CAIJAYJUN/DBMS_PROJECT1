from django import views
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.urls import path
from Publish import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^publish/add/$',views.addPublish),
    url(r'^publish/update/$',views.updatePublish),
    path('delete/<str:id>',views.deletePublish,name='delete'),
    url(r'^publish/search/$',views.searchPublish),
    url(r'^publish/publisherLogin/$',views.login_publisher),
    url(r'^publish/publisher_logout/$',views.logout_publisher),

    url(r'^publish/book_management/$',views.book_management),
    url(r'^publish/addAuthor/$',views.addAuthor),
    url(r'^publish/addBook/$',views.addBook),
    path('deleteBook/<str:id>',views.deleteBook,name='deleteBook'),

]+ static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT
    )
