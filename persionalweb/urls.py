from django.contrib import admin
from django.urls import path, include
from shares import views

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', views.index),
    path(r'gupiao/', views.gupiao),
    path(r'gupiao_ajax/', views.gupiao_ajax),
    path(r'gupiao/gainian/', views.gainian),
    path(r'gupiao/gainian_ajax/', views.gainian_ajax),
    path(r'seach_byname/', views.seach_byname),
    path(r'hangye/', views.hangye),
    path(r'hangye_ajax/', views.hangye_ajax),
]
