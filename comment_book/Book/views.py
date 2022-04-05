from django.shortcuts import render,redirect
from .models import Book
# Create your views here.
def main(request):
    All_book = Book.objects.all()
    
    
    return render(request,'main.html',locals())
