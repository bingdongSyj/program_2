import random
import string
import os
import re
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
# from admin_app.utils import checkMail,checkMobile
# Create your views here.
#生成一个验证码 并将图片，写出给浏览器
from admin_app.models import User


def getcaptcha(request):
    #从image.py中导入ImageCaptcha类，ImageCaptcha是图片验证码的核心类
    from captcha.image import ImageCaptcha
    #为验证码设置字体，获取项目目录下的字体文件
    imgage = ImageCaptcha(fonts=[os.path.abspath("fonts/segoeprb.ttf")])
    #随机码
    #大小写英文字母+数字，并随机取5位作为验证码
    code=random.sample(string.ascii_lowercase+string.ascii_uppercase+string.digits,3)
    #code是一个列表 用join转换成字符串
    #将验证码存入session，以备后续验证
    request.session["code"]="".join(code)
    #将生成的随机字符拼接成字符串，作为验证码图片中的文本
    data=imgage.generate("".join(code))
    #写出验证图片给客户端 告知浏览器，写出的内容是一图片
    return HttpResponse(data,"image/png")

#ajax异步验证验证码
def check_captcha(request):
    number=request.POST.get("number")
    num=request.session.get("code")
    if num.lower()==number.lower():
        return HttpResponse("ok")
    return HttpResponse("error")

# #ajax异步验证昵称
# def check_nike(request):
#     nike=request.POST.get("nike")
#     if not nike:
#         return HttpResponse("0")
#     return HttpResponse("1")
#
# #ajax异步验证password
# def check_pwd(request):
#     s1=(r'\W{6,20}')
#     password=request.POST.get("password")
#     if not password:
#         return HttpResponse("3")
#     elif len(password)<6:
#         return HttpResponse("0")
#     else:
#         if re.findall(s1,password,re.I) or password.isdigit() or password.isalpha():
#             return HttpResponse("2")
#         return HttpResponse("1")
#
def regist_page(request):
    return render(request,"admin_app/register.html")

def regist_logic(request):
    userid=request.POST.get('userid')
    usrtel=request.POST.get('usrtel')
    email=request.POST.get('email')
    psw=request.POST.get('psw')
    password=make_password(psw) #传入密文
    user=User(email=email,username=userid,password=password,phone=usrtel)
    user.save()
    request.session["name"]=usrtel
    return render(request, "admin_app/index.html")

def login_page(request):
    name=request.session.get("name")
    if name:
        return render(request,"admin_app/index.html",{"name":name})
    return render(request,"admin_app/index.html")

# def login_logic(request):
#     #接受参数
#     flag=request.GET.get("flag")
#     txtUsername=request.POST.get("txtUsername")
#     txtPassword=request.POST.get("txtPassword")
#     #是否7天内自动登录
#     autologin=request.POST.get("autologin")
#     user=User.objects.filter(email=txtUsername)
#     if user:
#         check=check_password(txtPassword,User.objects.get(email=txtUsername).password)
#         if check:
#             request.session["nike"] = User.objects.get(email=txtUsername).username
#             status=User.objects.get(email=txtUsername).status
#             if status:
#                 if autologin:
#                     request.session["name"]=txtUsername
#                 #根据flag进行判断跳转到哪 若为0，则从主页而来；若为1，则从购物车跳过来，强制登录
#                     if flag=="1":
#                         return redirect("order:settle_accounts")
#                     return redirect("all:main_page")
#             else:
#                 err2='邮箱验证错误，请重新注册！'
#                 return render(request, "admin_app/login.html", {"flag": flag, "err": err2})
#         else:
#             err = '密码错误，请重新登录!'
#             return render(request,"admin_app/login.html",{"flag":flag,"err":err})
#     err1 = '用户名错误，请重新登录!'
#     return render(request,"admin_app/login.html",{"flag":flag,"err":err1})
#
# def del_session(request):
#     del request.session["nike"]
#     return redirect("all:main_page")
#
#
#
