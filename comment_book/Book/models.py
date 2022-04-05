from email.mime import image
from turtle import title
from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from Publish.models import Publisher
def year_choices():
    return [(r,r) for r in range(1900, datetime.date.today().year)]
def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)  
# Create your models here.
class Book(models.Model):
    #書籍的資料表建立
    ISBN = models.CharField(max_length=13,primary_key=True,blank=False)
    title = models.CharField(max_length=30,blank=False)
    pubYear = models.IntegerField()
    bookProfile = models.CharField(max_length=250)
    language = models.CharField(choices=(("1",'中文'),("2",'西班牙語'),('3','英語'),('4','孟加拉語'),("5",'印地語／烏爾都語'),("6",'阿拉伯語')),blank=False,max_length=10)
    bookImage = models.ImageField(upload_to='image/')
    Publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE,related_name='publisher')
class Author(models.Model):
    
    id_num = models.CharField(max_length=30,primary_key=True,blank=False)
    name = models.CharField(max_length=10,blank=False)
    sex = models.CharField(choices=(("1",'女'),("2",'男'),("3",'其他')),max_length=3,blank=False)
    authorProfile = models.CharField(max_length=250)
    birthYear = models.IntegerField(choices=year_choices())
class authorWriteBook(models.Model):
    #多了“authorWriteBook_ID”，因為原本新增資料時有錯誤，"authorWriteBook_ID=author+book"
    authorWriteBook_ID = models.CharField(max_length=30,primary_key=True,blank=False)
    author = models.ForeignKey(Author,blank=True,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,blank=True,on_delete=models.CASCADE)
    class Meta:
        unique_together=(('author','book'),)