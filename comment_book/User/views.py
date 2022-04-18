

# Create your views here.
from audioop import add
import pwd
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.contrib import messages
import datetime
from Publish.models import Publisher
from Book.models import Book, Author, authorWriteBook
from User.models import User, BookList ,CommentBook,BookList,BookListIncludeBook


def year_choices():
    return [r for r in range(1900, datetime.date.today().year)]


def current_year():
    return datetime.date.today().year


def register(request):
    # 讀者註冊
    years = year_choices()
    if request.method == 'POST':
        id_num = request.POST['InputEmail']
        if User.objects.filter(id_num=id_num).exists():
            messages.success(request, "帳號已註冊")
            request.session.flush()
            return redirect('/comment_book/register/')
        pwd = request.POST['Password']
        name = request.POST['userName']
        addr = request.POST['address']
        year = request.POST['year']
        insertData = User.objects.create(id_num=id_num, passWord=make_password(
            pwd), name=name, location=addr, birthYear=year, indentify=1)
        insertData.save()
        request.session.flush()
        return redirect('/comment_book/register/')
    return render(request, 'register.html', locals())


def login(request):
    # 讀者登入
    if request.method == 'POST':
        id_num = request.POST['email']
        filter_ = User.objects.filter(id_num=id_num, indentify=1)
        if len(filter_) == 0:
            messages.success(request, "帳號不存在")
            return redirect('/comment_book/login/')
        else:
            pwd = request.POST['password']
            if(check_password(pwd, filter_[0].passWord) == False):
                messages.success(request, "密碼錯誤")

                return redirect('/comment_book/login/')
            else:
                request.session['register'] = True
                request.session['id_num'] = filter_[0].id_num
                request.session['name'] = filter_[0].name
                return redirect('/comment_book/main/')

    return render(request, 'login.html', locals())


def logout(request):
    # 讀者登出
    del request.session['register'], request.session['id_num'], request.session['name']
    return redirect('/comment_book/login/')

from django.db.models import Avg
def main(request):
    # 讀者登入後頁面
    if 'id_num' not in request.session:
        messages.success(request, "請先登入")
        return redirect('/comment_book/login/')

    user_name = User.objects.filter(
        id_num=request.session["id_num"]).all().first().name

    # book = Book.objects.raw(
    #     "SELECT * FROM BOOK_BOOK INNER JOIN (SELECT * FROM BOOK_AUTHORWRITEBOOK INNER JOIN BOOK_AUTHOR ON BOOK_AUTHORWRITEBOOK.AUTHOR_ID = BOOK_AUTHOR.ID_NUM) ON BOOK_BOOK.ISBN = BOOK_ID"
    # )

    book = Book.objects.raw(
        "SELECT * FROM BOOK_BOOK"
    )
    for i in book:
        i.name = ""
        i.avg_score = 0
        author = authorWriteBook.objects.raw(
            f"SELECT * FROM BOOK_AUTHORWRITEBOOK INNER JOIN BOOK_AUTHOR ON BOOK_AUTHORWRITEBOOK.AUTHOR_ID = BOOK_AUTHOR.ID_NUM WHERE BOOK_AUTHORWRITEBOOK.BOOK_ID = {i.ISBN}"
        )
        score = CommentBook.objects.filter(
            book=Book.objects.get(ISBN=i.ISBN)
        )
        i.avg_score = score.aggregate(Avg('star'))['star__avg']


        # print(author.columns)
        for j in author:
            # print(j.name)
            i.name += j.name+"、"

    return render(request, "main.html", locals())

# def searchBook(request):
    
#     return render(request, "searchBook.html", locals())
from django.db.models import Q
def searchBook(request):
    if 'id_num' not in request.session:
        messages.success(request, "請先登入")
        return redirect('/comment_book/login/')
    if request.method == 'GET':
        key = request.GET.get('keyWord')
        print(key)
        # result = Book.objects.all()
        try:
            result = Book.objects.filter(title__icontains=key)
            print(result)
            for i in result:
                i.avg_score=0
                score = CommentBook.objects.filter(
                    book=Book.objects.get(ISBN=i.ISBN)
                )
                i.avg_score = score.aggregate(Avg('star'))['star__avg']
                author = authorWriteBook.objects.raw(
                    f"SELECT * FROM BOOK_AUTHORWRITEBOOK INNER JOIN BOOK_AUTHOR ON BOOK_AUTHORWRITEBOOK.AUTHOR_ID = BOOK_AUTHOR.ID_NUM WHERE BOOK_AUTHORWRITEBOOK.BOOK_ID = {i.ISBN}"
                )
                i.name=""
                for j in author:
                    print(j.name)
                    i.name += j.name+"、"
                print(i.name)
            
            return render(request,"searchBook.html",{'result':result,'input':key})
        except:
            
            return render(request, "searchBook.html", {'result':None,'input':""})
    
    return render(request, "searchBook.html", locals())


def listUserBook(request):
    if 'id_num' not in request.session:
        messages.success(request, "請先登入")
        return redirect('/comment_book/login/')
    user_name = User.objects.filter(
        id_num=request.session["id_num"]).all().first().name
    bookList = BookList.objects.filter(
        user = User.objects.get(id_num=request.session['id_num'])
    )
    
    for i in bookList:
        book = BookListIncludeBook.objects.filter(
            user_name = i,
        )
        books=[]
        for j in book:

            # print(j)
            
            
            author = authorWriteBook.objects.raw(
                f"SELECT * FROM BOOK_AUTHORWRITEBOOK INNER JOIN BOOK_AUTHOR ON BOOK_AUTHORWRITEBOOK.AUTHOR_ID = BOOK_AUTHOR.ID_NUM WHERE BOOK_AUTHORWRITEBOOK.BOOK_ID = {j.book.ISBN}"
            )
            j.book.name=""
            for k in author:
                j.book.name += k.name+"、"
            books.append(j.book)
            # print(j.book.ISBN)
        i.books = books
        # for k in i.books:
        #     print(k.ISBN)

    return render(request, "getUserList.html", locals())


def build_bookshelf(request,isbn):
    #加入書籍至清單
    # user_name = User.objects.filter(
    #     id_num=request.session["id_num"]).all().first().name
    # if request.method == "POST":
    #     name = request.POST["name"]
    #     if BookList.objects.filter(user=request.session["id_num"]).exists():
    #         messages.success(request, "書籍已存在")
    # name = request.POST["name"]
    # isbn = request.POST["ISBN"]
    if 'id_num' not in request.session:
        messages.success(request, "請先登入")
        return redirect('/comment_book/login/')
    id_num = request.session["id_num"]
    user = User.objects.get(id_num=id_num)
    user_name = User.objects.filter(
        id_num=request.session["id_num"]).all().first().name
    
    bookList = BookList.objects.filter(user=user)
    ISBN = isbn
    book = Book.objects.get(ISBN=ISBN)
    # print("hello")
    # print(request.POST.getlist("listName"))
    if request.method == "POST":

        # book_list=request.POST.getlist("listName")
        
        # book_list=book_list.extend(request.POST.getlist("listName_select"))
        
        for i in request.POST.getlist("listName"):
            if i=="":
                break
            try:
                con = BookList(user = user, name = i, buildDate=datetime.datetime.now())
                con.save()
                con = BookListIncludeBook(user_name = con,book=book)
                con.save()
            except:
                pass
        for i in request.POST.getlist("listName_select"):
            # print(i)
            try:
                print(i)
                # con = BookList(user = user, name = i, buildDate=datetime.datetime.now())
                # con.save()
                con = BookList.objects.get(user = user,name=i)
                # print(con)
                con = BookListIncludeBook(user_name = con,book=book)
                con.save()
            except:
                pass
        return redirect("/comment_book/main/")


    return render(request, "bookshelf.html", locals())




def user_comment(request, isbn):
    #使用者評論
    if 'id_num' not in request.session:
        messages.success(request, "請先登入")
        return redirect('/comment_book/login/')

    ISBN = isbn
    id_num = request.session["id_num"]
    user_name = User.objects.filter(
        id_num=request.session["id_num"]).all().first().name
    user = User.objects.get(id_num=id_num)
    book = Book.objects.get(ISBN=ISBN)
    allComment = CommentBook.objects.filter(book = book)
    if request.method == "POST":
        star = request.POST["star"]
        
        comments = request.POST["comments"]
        if CommentBook.objects.filter(user=user,book=book).exists():
            CommentBook.objects.filter(user=user,book=book).update(comments=comments, star=star)
            return redirect("/comment_book/main/")
        

        
        # 評論書籍
        con = CommentBook(user=user, book=book, comments=comments, star=star)
        con.save()
        # request.session.flush()
        return redirect("/comment_book/main/")

    return render(request, "user_comment.html" ,locals())
    

#####
def register_admin(request):
    # 管理者註冊
    years = year_choices()
    if request.method == 'POST':
        id_num = request.POST['InputEmail']
        if User.objects.filter(id_num=id_num).exists():
            messages.success(request, "帳號已註冊")
            request.session.flush()
            return redirect('/comment_book/registerAdmin/')

        pwd = request.POST['Password']
        name = request.POST['userName']
        addr = request.POST['address']
        year = request.POST['year']
        insertData = User.objects.create(id_num=id_num, passWord=make_password(
            pwd), name=name, location=addr, birthYear=year, indentify=0)
        insertData.save()
        request.session.flush()
        return redirect('/comment_book/registerAdmin/')

    return render(request, 'register.html', locals())


def adminLogin(request):
    # 管理者登入
    if request.method == 'POST':
        id_num = request.POST['email']
        filter_ = User.objects.filter(id_num=id_num, indentify=0)
        if len(filter_) == 0:
            messages.success(request, "帳號不存在")
            return redirect('/comment_book/admin_login/')
        else:
            pwd = request.POST['password']
            if(check_password(pwd, filter_[0].passWord) == False):
                messages.success(request, "密碼錯誤")
                return redirect('/comment_book/admin_login/')
            else:
                request.session['registerAdmin'] = True
                request.session['id_numAdmin'] = filter_[0].id_num
                request.session['nameAdmin'] = filter_[0].name
                return redirect('/comment_book/main_manage/')

    return render(request, 'adminLogin.html', locals())


def adminLogout(request):
    # 管理者登出
    del request.session['registerAdmin'], request.session['id_numAdmin'], request.session['nameAdmin']
    return redirect('/comment_book/admin_login/')


def mainManage(request):
    # 進入管理者頁面
    if 'id_numAdmin' not in request.session:

        messages.success(request, "沒有權限，請先登入")
        return redirect('/comment_book/admin_login/')
    publisher = Publisher.objects.all()
    return render(request, 'main_admin.html', locals())
