from django.contrib import admin

from .models import User,BookList,BookListIncludeBook,CommentBook

# Register your models here.
admin.site.register(User)
admin.site.register(BookList)
admin.site.register(BookListIncludeBook)
admin.site.register(CommentBook)
