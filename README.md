
<h1 align="center">CodeAnswer</h1>
<p align="center">
  Find solutions faster
  <br>
    <a href="https://www.python.org/downloads/release/python-362/">
    <img src="https://img.shields.io/badge/python-3.8.0-blue.svg?style=flat-square" alt="Python 3.8.0" />
  </a>
  <a href="https://www.djangoproject.com/">
    <img src="https://img.shields.io/badge/django-3.2.9-blue.svg?style=flat-square" alt="Django 3.2.9" />
  </a>
  <a href="https://github.com/harmfl/AI_draw/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License" />
  </a>
  <!-- 插入徽章 -->
  <br />


### 开始部署：

（1）创建环境
```sh
conda create -n your_envirment python==3.8
```
(2)激活环境
```sh
conda activate your_envirment
```
(3)到下载项目对应的地址上
```sh
cd your_path
```
5.下载所需要的包
```sh
pip install -r requirement.txt
```
6.打开项目的ai_draw文件夹
配置settings
### 设置为mysql登录
```sh
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # 设置为 MySQL
        'NAME': 'CodeAnswer',                    # 数据库名称
        'USER': 'root',                       # 数据库用户名
        'PASSWORD': 'root',                   # 数据库密码
        'HOST': 'localhost',                  # 数据库主机，通常是 localhost
        'PORT': '3306',                       # 数据库端口，MySQL 默认是 3306
    }
}
```
7.执行迁移指令
（1）生成迁移表
```sh
python manage.py makemigrations
```
（2）执行迁移命令
```sh
python manage.py migrate
```
8.打开终端执行命令启动项目
```sh
 python manage.py runserver
```
