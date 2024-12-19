from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
import subprocess
from Core.settings import *
from threading import Thread
import json
import socket
from channels.layers import get_channel_layer
from Login.models import *
from .models import *
from django.contrib import messages

def no_next_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_view')  # 自定义登录视图
        return view_func(request, *args, **kwargs)
    return _wrapped_view

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

@no_next_login_required
def index(request):
    username = request.user.username
    return render(request,'html/index.html',context={'username':username})

@no_next_login_required
def spider_post_view(request):
    user = request.user
    username = user.username
    if request.method == "POST":
        try:
            num_of_crawl = Num_of_Crawl.objects.get(user=user.customuser)  # 使用 CustomUser 作为外键
        except Exception:
            num_of_crawl = None  # 如果没有找到 Num_of_Crawl 实例，设置为 None
            print('查询不到num_of_crawl，爬取失败')
            return render(request,'html/index.html',context={'username':username})
        # 获取表单数据
        else:
            query = request.POST.get('query')  # 获取表单数据
            if query:
                # test_num=5
                # CSDN_thread = Thread(target=run_CSDN_script, args=(request,query,str(test_num)))
                # CSDN_thread.start()
                # print('-'*25,'已启动爬虫脚本','-'*25)
                try:
                    subprocess.run([
                        'python', CSDN_REP,
                        '--key_text', query,
                        '--num', str(num_of_crawl.csdn_count),
                    ], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Subprocess failed with error: {e}")
                result_dir = os.path.join(MEDIA_ROOT, 'CSDN.json')
                with open(result_dir, "r", encoding="utf-8") as f:
                    CSDN_data = json.load(f)
                titles = [item['title'] for item in CSDN_data]
                descriptions = [item['description'] for item in CSDN_data]
                urls = [item['url'] for item in CSDN_data]
                CSDN_combined_data = []
                for title, description, url in zip(titles, descriptions, urls):
                    CSDN_combined_data.append({
                        'title': title,
                        'description': description,
                        'url': url
                    })

                try:
                    subprocess.run([
                        'python', CNBLOGS_REP,
                        '--key_text', query,
                        '--num', str(num_of_crawl.cnblogs_count),
                    ], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Subprocess failed with error: {e}")
                result_dir = os.path.join(MEDIA_ROOT, 'CNBLOGS.json')
                with open(result_dir, "r", encoding="utf-8") as f:
                    CNBLOGS_data = json.load(f)
                titles = [item['title'] for item in CNBLOGS_data]
                descriptions = [item['description'] for item in CNBLOGS_data]
                urls = [item['url'] for item in CNBLOGS_data]
                CNBLOGS_combined_data = []
                for title, description, url in zip(titles, descriptions, urls):
                    CNBLOGS_combined_data.append({
                        'title': title,
                        'description': description,
                        'url': url
                    })

                try:
                    subprocess.run([
                        'python', JUEJIN_REP,
                        '--key_text', query,
                        '--num', str(num_of_crawl.juejin_count),
                    ], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Subprocess failed with error: {e}")
                result_dir = os.path.join(MEDIA_ROOT, 'JUEJIN.json')
                with open(result_dir, "r", encoding="utf-8") as f:
                    JUEJIN_data = json.load(f)
                titles = [item['title'] for item in JUEJIN_data]
                descriptions = [item['description'] for item in JUEJIN_data]
                urls = [item['url'] for item in JUEJIN_data]
                JUEJIN_combined_data = []
                for title, description, url in zip(titles, descriptions, urls):
                    JUEJIN_combined_data.append({
                        'title': title,
                        'description': description,
                        'url': url
                    })

                try:
                    subprocess.run([
                        'python', GITHUB_REP,
                        '--key_text', query,
                        '--num', str(num_of_crawl.github_count),
                    ], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Subprocess failed with error: {e}")
                result_dir = os.path.join(MEDIA_ROOT, 'GITHUB.json')
                with open(result_dir, "r", encoding="utf-8") as f:
                    GITHUB_data = json.load(f)
                titles = [item['title'] for item in GITHUB_data]
                descriptions = [item['description'] for item in GITHUB_data]
                urls = [item['url'] for item in GITHUB_data]
                GITHUB_combined_data = []
                for title, description, url in zip(titles, descriptions, urls):
                    GITHUB_combined_data.append({
                        'title': title,
                        'description': description,
                        'url': url
                    })

                return render(request, 'html/index.html',
                              context={
                                  'username': username,
                                  'CSDN_data':CSDN_combined_data,
                                  'CNBLOGS_data':CNBLOGS_combined_data,
                                  'JUEJIN_data':JUEJIN_combined_data,
                                  'GITHUB_data':GITHUB_combined_data,
                              })

    # 如果是 GET 请求，返回空表单
    return render(request, 'html/index.html')

@no_next_login_required
def run_CSDN_script(request,key_text,num):
    try:
        subprocess.run([
            'python', CSDN_REP,
            '--key_text', key_text,
            '--num',num,
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Subprocess failed with error: {e}")
    result_dir = os.path.join(MEDIA_ROOT, 'CSDN.json')
    with open(result_dir, "r", encoding="utf-8") as f:
        CSDN_data = json.load(f)
    titles = [item['title'] for item in CSDN_data]
    descriptions = [item['description'] for item in CSDN_data]
    urls = [item['url'] for item in CSDN_data]
    CSDN_combined_data = []
    for title, description, url in zip(titles, descriptions, urls):
        CSDN_combined_data.append({
            'title': title,
            'description': description,
            'url': url
        })
    # channel_layer = get_channel_layer()
    # channel_layer.group_send(
    #     'data_group',  # 群组名称
    #     {
    #         'type': 'send_data',  # 消息类型
    #         'data': CSDN_combined_data  # 要发送的数据
    #     }
    # )
    # print(CSDN_combined_data)
    # for item in CSDN_combined_data:
    #     print(item)

@no_next_login_required
def sp_setting_view(request):
    user = request.user
    username = request.user.username
    try:
        num_of_crawl = Num_of_Crawl.objects.get(user=user.customuser)  # 使用 CustomUser 作为外键
    except Num_of_Crawl.DoesNotExist:
        num_of_crawl = None  # 如果没有找到 Num_of_Crawl 实例，设置为 None

    if request.method == "POST":
        CSDN_n = request.POST.get("CSDN_num")
        Github_n = request.POST.get("Github_num")
        CNBLOGS_n = request.POST.get("CNBLOGS_num")
        JUEJIN_n = request.POST.get("JUEJIN_num")
        if all([is_valid_number(CSDN_n), is_valid_number(Github_n), is_valid_number(CNBLOGS_n),
                is_valid_number(JUEJIN_n)]):
            # 如果输入有效，更新对应的 Num_of_Crawl 实例
            if num_of_crawl:
                num_of_crawl.csdn_count = int(CSDN_n)
                num_of_crawl.github_count = int(Github_n)
                num_of_crawl.cnblogs_count = int(CNBLOGS_n)
                num_of_crawl.juejin_count = int(JUEJIN_n)
                num_of_crawl.save()
                messages.error(request, "设置已更新！")
            else:
                messages.error(request, "请填写合理的数字")
        else:
            # 如果任何字段无效，显示错误消息
            messages.error(request, "请输入大于 0 的正整数！")

            # 保存完成后，重定向到当前页面，防止重复提交
        return redirect('sp_setting_view')

    return render(request,'html/sp_setting.html',context={'username':username,'num_of_crawl':num_of_crawl})


def is_valid_number(value):
    try:
        # 转换为整数并检查是否大于 0
        num = int(value)
        return num > 0
    except (ValueError, TypeError):
        # 如果转换失败（如小数或非数字字符），返回 False
        return False