import imp
from secrets import choice
from django.db import models
import datetime
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from Book.models import Book
def year_choices():
    return [(r,r) for r in range(1900, datetime.date.today().year)]
def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)  
# Create your models here.
class User (models.Model):
    id_num = models.CharField(max_length=30,primary_key=True,blank=False)
    passWord = models.CharField(max_length=100,blank=False)
    name = models.CharField(max_length=10,blank=False)
    location = models.CharField(max_length=30)
    birthYear = models.IntegerField(choices=year_choices())
    indentify = models.BooleanField(blank=False,default=False)

class BookList(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    name = models.CharField(max_length=10,blank=False)
    buildDate = models.DateTimeField()
    class Meta:
        unique_together=(('user','name'))
class BookListIncludeBook(models.Model):
    user_name = models.ForeignKey(BookList,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    class Meta:
        unique_together=(('user_name','book'))
class CommentBook(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    comments = models.CharField(max_length=300,blank=False)
    star = models.IntegerField(validators=[MaxValueValidator(10),MinValueValidator(0)])
    class Meta:
        unique_together=(('user','book'))