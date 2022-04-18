from django.shortcuts import render
from django.shortcuts import redirect,render
from django.contrib.auth.hashers import make_password, check_password
from .models import Publisher
from Book.models import Author,Book,authorWriteBook
from django.contrib import messages
import datetime
from django.core.files.storage import FileSystemStorage
# Create your views here.


########################    以下管理者權限下使用     ######################
def addPublish(request):
    #新增出版社
    if request.session['registerAdmin']==False:
        #利用session確認是否有連線，session會放使用者登入資訊，在一定時間內使用者不需重新登入即可有權限，但一個時間點過後，session會失效
        messages.success(request,"沒有權限，請先登入")
        return redirect('/comment_book/admin_login/')
    if request.method == "POST":
        id_num = request.POST['InputEmail']
        if Publisher.objects.filter(id_num=id_num).exists():
            messages.success(request, "出版社已存在")
            request.session.flush()
            return redirect('/comment_book/main_manage/')
        pwd = request.POST['Password']
        name = request.POST['name']
        tel = request.POST['tel']
        email = request.POST['InputEmail']
        insertData = Publisher.objects.create(id_num=id_num,passWord=make_password(pwd),name=name,tel=tel,emailAddr=email)
        insertData.save()
        return redirect('/comment_book/main_manage/')
    # return render(request,'addPublish.html',locals())

def updatePublish(request):
    #更新出版社資料
    if request.session['registerAdmin']==False:
        messages.success(request,"沒有權限，請先登入")
        return redirect('/comment_book/admin_login/')
    publisher = Publisher.objects.all()
    if request.method == "POST":
        pwd = request.POST['PasswordUpdate']
        name = request.POST['selectPublisher']
        tel = request.POST['telUpdate']
        email = request.POST['InputEmailUpdate']
        if len(request.POST['PasswordUpdate'])>0:
            Publisher.objects.filter(name=name).update(id_num=email,passWord=make_password(pwd),tel=tel,emailAddr=email)
        else :
            Publisher.objects.filter(name=name).update(id_num=email,tel=tel,emailAddr=email)


        
    return redirect('/comment_book/main_manage/')

def deletePublish(request,id):
    #刪除出版社
    obj=Publisher.objects.get(name=id)
    obj.delete()
    
    return redirect('/comment_book/main_manage/')






########################    以下出版社權限下使用     ######################



def book_management(request):
    # 書籍作者管理主頁
    if 'publish_id' not in request.session:
        messages.success(request,"沒有權限，請先登入")
        return redirect('/comment_book/publish/publisherLogin/')
    years = year_choices()
    publisher =  Publisher.objects.all()
    author =Author.objects.all()
    book = Book.objects.all()
    hello_user = "Hello!    "+request.session['publish_name']+"  出版社"

    return render(request,"publisherManagement.html",locals())#publisherManagement.html 會被塞入多個功能

def addAuthor(request):
    # 新增不存在資料庫的作家
    if request.method == "POST":
        id_num = request.POST['AuthorEmail']
        if Author.objects.filter(id_num=id_num).exists():
            messages.success(request, "作者已存在")
            return redirect('/comment_book/publish/book_management/')
        name = request.POST['authorName']
        sex = request.POST['selectSex']
        desc = request.POST['authorDesc']
        year = request.POST['authorYear']
        insertData = Author.objects.create(id_num=id_num,name=name,sex=sex,authorProfile=desc,birthYear=year)
        insertData.save()

    return redirect('/comment_book/publish/book_management/')
def addBook(request):
    #上架書籍
    if request.method == "POST":
        isbn = request.POST['ISBN']
        if Book.objects.filter(ISBN=isbn).exists():
            messages.success(request, "書籍已存在")
            return redirect('/comment_book/publish/book_management/')
        name = request.POST['bookName']
        year = request.POST['publishYear']
        lang = request.POST['selectLang']
        authors = request.POST.getlist('selectAuthor')
        desc = request.POST['bookDesc']
        img = request.FILES['bookImage']
        
        insertData = Book.objects.create(
            ISBN=isbn,title=name,
            pubYear=year,
            bookProfile=desc,
            language=lang,
            bookImage=img,
            Publisher=Publisher.objects.get(id_num=request.session['publish_id']))
        insertData.save()
        for i in authors:

            insertData_ = authorWriteBook.objects.create(
                #這邊有個bug，還無法解決，所以我在資料庫加入一個“authorWriteBook_ID”的主鍵欄位
                authorWriteBook_ID = i+isbn,
                author = Author.objects.get(name=i),
                book = Book.objects.get(ISBN=isbn)
                )
            insertData_.save()

    return redirect('/comment_book/publish/book_management/')
def deleteBook(request,id):
    #刪除書籍

    obj=Book.objects.get(ISBN=id)
    obj.delete()

    return redirect('/comment_book/publish/book_management/')
def searchPublish(request):
    
    return

def year_choices():
    # 用來秀出西元年的選擇表單
    return [r for r in range(1900, datetime.date.today().year+1)]
def current_year():
    return datetime.date.today().year
def logout_publisher(request):
    if 'publish_id' not in request.session:
        return redirect('/comment_book/publish/publisherLogin/')
    del request.session['publish_id']
    
    return redirect('/comment_book/publish/publisherLogin/')
    

def login_publisher(request):
    #出版社登入，須先登入才可以進入管理頁面
    if request.method =='POST':
        id_num=request.POST['email']
        filter_=Publisher.objects.filter(id_num=id_num)
        if len(filter_)==0:
            messages.success(request,"帳號不存在")
            return redirect('/comment_book/publish/publisherLogin/')
        else:
            pwd=request.POST['password']

            if(check_password(pwd,filter_[0].passWord)==False):
                messages.success(request,"密碼錯誤")
                return redirect('/comment_book/publish/publisherLogin/')
            else:
                request.session['publish_id'] = id_num
                
                request.session['publish_name'] = filter_[0].name
                hello_user = "Hello! "+request.session['publish_name']
                
                return redirect('/comment_book/publish/book_management/')

    return render(request,'PublishLogin.html',locals())

from pyecharts.charts import Bar
from pyecharts import options as opts
# from __future__ import unicode_literals
import math
from Book.models import Book, Author, authorWriteBook
from User.models import User, BookList ,CommentBook,BookList,BookListIncludeBook 
from django.db.models import Avg, Count, Min, Sum
from django.http import HttpResponse
from django.template import loader

REMOTE_HOST = "https://pyecharts.github.io/assets/js"
def plotBar(request):
    if 'publish_id' not in request.session:
        return redirect('/comment_book/publish/publisherLogin/')
    template = loader.get_template('barChar.html')
    publish = Publisher.objects.get(id_num = request.session['publish_id'])
    book = Book.objects.filter(Publisher=publish)
    bookName=[]
    bookSumScore=[]
    bookAvgScore=[]
    bookCommentCount=[]
    for i in book:
        bookName.append(i.title)
        Allstar = CommentBook.objects.filter(book = i)

        bookSumScore.append(Allstar.aggregate(Sum('star'))['star__sum'])
        bookAvgScore.append(Allstar.aggregate(Avg('star'))['star__avg'])
        bookCommentCount.append(Allstar.aggregate(Count('star'))['star__count'])
    bookSumScore_=[]
    bookAvgScore_=[]
    bookCommentCount_=[]
    for i,j,k in zip(bookSumScore,bookAvgScore,bookCommentCount):
        if i :
            bookSumScore_.append(i)
            bookAvgScore_.append(j)
            bookCommentCount_.append(k)
        else:
            bookSumScore_.append(0)
            bookAvgScore_.append(0)
            bookCommentCount_.append(0)
    bookSumScore = bookSumScore_
    bookAvgScore = bookAvgScore_
    bookCommentCount = bookCommentCount_

    for i in range(len(bookName)):
        n = ""
        for j in range(0,len(bookName[i]),5):
            n+=bookName[i][j:j+5]+"\n"
        bookName[i] = n


    # bookName = [i[0:6]+'\n'+i[6:] for i in bookName]
    print(bookName,bookSumScore)
    bar1 = Bar().add_xaxis(
        bookName
    ).add_yaxis(
        '書籍總分',bookSumScore
    ).add_yaxis(
        '書籍平均分',bookAvgScore
    ).add_yaxis(
        '評分次數' ,bookCommentCount
    ).set_global_opts(
        title_opts=opts.TitleOpts(title="書籍評分", subtitle="單位： 分")
    )
    


    context = dict(
        bar_data=bar1.dump_options(),
        # host=REMOTE_HOST,
        # script_list=bar.get_js_dependencies(),
    )
    # context=bar.dump_options()
    
    return HttpResponse(template.render(context, request))
    # print(bar.dump_options())
    # return HttpResponse(bar.render_embed())

# from django_echarts.starter.sites import DJESite
# from django_echarts.entities import Copyright
# from pyecharts import options as opts
# from pyecharts.charts import Bar
# from Book.models import Book, Author, authorWriteBook
# from User.models import User, BookList ,CommentBook,BookList,BookListIncludeBook 
# from django.db.models import Avg, Count, Min, Sum
# site_obj = DJESite(site_title='書籍分數統計')
# chart_description = '長條圖：書籍總分'

# @site_obj.register_chart(title='書籍總分', description = chart_description)
# def plotSumScore(request):
#     if 'publish_id' not in request.session:
#         return redirect('/comment_book/publish/publisherLogin/')
#     publish = Publisher.objects.get(id_num = request.session['publish_id'])
#     book = Book.objects.filter(Publisher=publish)
#     bookName=[]
#     bookSumScore=[]
#     for i in book:
#         bookName.append(i.title)
#         Allstar = CommentBook.objects.filter(book = i)

#         bookSumScore.append(Allstar.aggregate(Sum('star')))
#     bar = Bar().add_xaxis(
#         bookName
#     ).add_yaxis(
#         '書籍總分',bookSumScore
#     ).set_global_opts(
#         title_opts=opts.TitleOpts(title="書籍總分", subtitle="單位： 分"),
#         visualmap_opts=opts.VisualMapOpts(is_show=True, max_=100, min_=0)).set_series_opts(
#         markline_opts=opts.MarkLineOpts(
#             data=[
                
#             ]
#         )
#     )



#     return bar
