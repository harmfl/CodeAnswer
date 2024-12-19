from django.urls import path, include
# from .views import login_view, register_view, home_view
from .views import *
from django.conf import settings

urlpatterns = [
    path('',login_view,name='login_view'),
    path('register/',register_view,name='register_view'),
]
