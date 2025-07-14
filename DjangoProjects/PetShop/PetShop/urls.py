"""
URL configuration for PetShop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from PetShopApp.views import contact,index,about,staff,private,logout,login,address

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index , name='index'),
    re_path('^contact/$',contact, name='contact'),
    re_path('^about/$',about, name='about'),
    re_path(r'^staff/(?P<status>\w+)/$',staff,name='staff'),
    re_path(r'^staff/$', staff, name='staff_no_status'),
    re_path(r'^private/$',private, name='private_no_status'),
    re_path(r'private/(?P<status>\w+)/$',private,name='private'),
    re_path(r'^logout/$',logout, name='logout'),
    re_path(r'^login/$',login, name='login'),
    re_path(r'^delivery/$',address,name='delivery'),
]
