import imp
from django.contrib import admin
from .models import Book,authorWriteBook,Author
# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(authorWriteBook)

