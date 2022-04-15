# Create your views here.
from audioop import add
import pwd
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from django.contrib import messages
import datetime
from Publish.models import Publisher
from Book.models import Book
from User.models import User, BookList, CommentBook
from django import template
from django.shortcuts import render_to_response


def year_choices():
    return [r for r in range(1900, datetime.date.today().year)]


def current_year():
    return datetime.date.today().year


def register(request):
    # 讀者註冊
    years = year_choices()
    if request.method == "POST":
        id_num = request.POST["InputEmail"]
        if User.objects.filter(id_num=id_num).exists():
            messages.success(request, "帳號已註冊")
            request.session.flush()
            return redirect("/comment_book/register/")
        pwd = request.POST["Password"]
        name = request.POST["userName"]
        addr = request.POST["address"]
        year = request.POST["year"]
        insertData = User.objects.create(
            id_num=id_num,
            passWord=make_password(pwd),
            name=name,
            location=addr,
            birthYear=year,
            indentify=1,
        )
        insertData.save()
        request.session.flush()
        return redirect("/comment_book/register/")
    return render(request, "register.html", locals())


def login(request):
    # 讀者登入
    if request.method == "POST":
        id_num = request.POST["email"]
        filter_ = User.objects.filter(id_num=id_num, indentify=1)
        if len(filter_) == 0:
            messages.success(request, "帳號不存在")
            return redirect("/comment_book/login/")
        else:
            pwd = request.POST["password"]
            if check_password(pwd, filter_[0].passWord) == False:
                messages.success(request, "密碼錯誤")
                return redirect("/comment_book/login/")
            else:
                request.session["register"] = True
                request.session["id_num"] = filter_[0].id_num
                request.session["name"] = filter_[0].name
                return redirect("/comment_book/main/")

    return render(request, "login.html", locals())


def main(request):
    # 讀者登入後頁面
    user_name = User.objects.filter(id_num=request.session["id_num"]).all().first().name
    book = Book.objects.raw(
        "SELECT * FROM (BOOK_BOOK NATURAL JOIN BOOK_AUTHORWRITEBOOK) NATURAL JOIN BOOK_AUTHOR"
    )
    return render(request, "main.html", locals())


def build_bookshelf(request):
    user_name = User.objects.filter(id_num=request.session["id_num"]).all().first().name
    # if request.method == "POST":
    # name = request.POST["name"]

    # name = request.POST["name"]
    # isbn = request.POST["ISBN"]

    return render(request, "bookshelf.html", locals())


def user_comment(request):
    if request.method == "POST":
        ISBN = request.POST["ISBN"]

        if not Book.objects.filter(ISBN=ISBN).exists():
            messages.success(request, "沒這本書")
            request.session.flush()
            return redirect("/comment_book/user_comment/")

        title = request.POST["title"]
        star = request.POST["star"]
        id_num = request.POST["email"]
        comments = request.POST["comments"]

        user = User.objects.get(id_num=id_num)
        book = Book.objects.get(ISBN=ISBN)
        # 評論書籍
        con = CommentBook(user=user, book=book, comments=comments, star=star)
        con.save()
        request.session.flush()
        return redirect("/comment_book/user_comment/")

    return render(request, "user_comment.html", locals())


def logout(request):
    # 讀者登出
    del request.session["register"], request.session["id_num"], request.session["name"]
    return redirect("/comment_book/login/")


def register_admin(request):
    # 管理者註冊
    years = year_choices()
    if request.method == "POST":
        id_num = request.POST["InputEmail"]
        if User.objects.filter(id_num=id_num).exists():
            messages.success(request, "帳號已註冊")
            request.session.flush()
            return redirect("/comment_book/registerAdmin/")

        pwd = request.POST["Password"]
        name = request.POST["userName"]
        addr = request.POST["address"]
        year = request.POST["year"]
        insertData = User.objects.create(
            id_num=id_num,
            passWord=make_password(pwd),
            name=name,
            location=addr,
            birthYear=year,
            indentify=0,
        )
        insertData.save()
        request.session.flush()
        return redirect("/comment_book/registerAdmin/")

    return render(request, "register.html", locals())


def adminLogin(request):
    # 管理者登入
    if request.method == "POST":
        id_num = request.POST["email"]
        filter_ = User.objects.filter(id_num=id_num, indentify=0)
        if len(filter_) == 0:
            messages.success(request, "帳號不存在")
            return redirect("/comment_book/admin_login/")
        else:
            pwd = request.POST["password"]
            if check_password(pwd, filter_[0].passWord) == False:
                messages.success(request, "密碼錯誤")
                return redirect("/comment_book/admin_login/")
            else:
                request.session["registerAdmin"] = True
                request.session["id_numAdmin"] = filter_[0].id_num
                request.session["nameAdmin"] = filter_[0].name
                return redirect("/comment_book/main_manage/")

    return render(request, "adminLogin.html", locals())


def adminLogout(request):
    # 管理者登出
    del (
        request.session["registerAdmin"],
        request.session["id_numAdmin"],
        request.session["nameAdmin"],
    )
    return redirect("/comment_book/admin_login/")


def mainManage(request):
    # 進入管理者頁面
    if "id_numAdmin" not in request.session:

        messages.success(request, "沒有權限，請先登入")
        return redirect("/comment_book/admin_login/")
    publisher = Publisher.objects.all()
    return render(request, "main_admin.html", locals())
