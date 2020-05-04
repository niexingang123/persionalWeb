from django.contrib import admin
from django.urls import path, include
from shares import views

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', views.index),
    path(r'gupiao/', views.gupiao),
    path(r'gupiao/gainian/', views.gainian),
    path(r'seach_byname/', views.seach_byname),
    path(r'gupiao/hangye/', views.hangye),
]
