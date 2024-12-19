from django.urls import path
# from .views import login_view, register_view, home_view
from .views import *
from django.conf import settings

urlpatterns = [
    path('',index,name='index_view'),
    path('spider_post',spider_post_view,name='spider_post_view'),
    path('sp_setting',sp_setting_view,name='sp_setting_view'),
]
