from django.shortcuts import render,redirect
import socket
from Main.models import Num_of_Crawl
from .models import *
from django.contrib.auth import authenticate,login
from django.contrib import messages

# Create your views here.
def get_local_ip():
    """获取服务器的局域网IP地址"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 连接到外部服务器（不实际发送数据），以获取局域网IP
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def login_view(request):
    if request.method == "POST":
        account = request.POST.get("account")
        password = request.POST.get("password")
        if password and account:
            try:
                user = CustomUser.objects.get(username=account,password=password)
            except CustomUser.DoesNotExist:
                messages.error(request, "账号或密码错误")
                return redirect('login_view')
            else:
                user = authenticate(request, username=account, password=password)
                login(request, user)
                return redirect('index_view')

    return render(request, 'html/login.html')

def register_view(request):
    if request.method == "POST":
        account = request.POST.get("account")
        password = request.POST.get("password")
        ensure_password = request.POST.get("ensure_password")
        if User.objects.filter(username=account).exists():
            messages.error(request,"已存在同名账号")
        else:
            if password and account:
                if ensure_password == password:
                    user = User.objects.create_user(username=account, password=password)
                    custom_user = CustomUser.objects.create(username=account, password=password, user=user)
                    Num_of_Crawl.objects.create(user=custom_user)
                    messages.error(request,"账号创建成功")
                    return redirect('login_view')
                else:
                    messages.error(request,"两次密码不一样")
            else:
                messages.error(request,"请输入账号和密码")
    return render(request, 'html/register.html')
