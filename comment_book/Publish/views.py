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
    return redirect('/comment_book/publish/book_management/')
def searchPublish(request):
    
    return

def year_choices():
    # 用來秀出西元年的選擇表單
    return [r for r in range(1900, datetime.date.today().year+1)]
def current_year():
    return datetime.date.today().year


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
                return redirect('/comment_book/publish/book_management/')

    return render(request,'PublishLogin.html',locals())

    

