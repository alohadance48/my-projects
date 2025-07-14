from django.http import HttpResponse
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.template.response import TemplateResponse
from django.shortcuts import render
from datetime import datetime

# Create your views here.


def index(request):
    book_list = ['Техническая литература','Фантастика','Сказки','Сборники стихов']
    date = {"book_list":book_list,'time':datetime.now()}
    return TemplateResponse(request, 'BookShopapp/index.html',date)

def contact(request):
    contact_list = ['github:alohadance48','email:afonskiy.vlad@mail.ru']
    date = {"contact_list":contact_list}
    return TemplateResponse(request, 'BookShopapp/contact.html',date)

def about(request):
    info = ['Программист','Playboy','Миллиардер','Скромный парень']
    date = {"about_list":info}
    return TemplateResponse(request, 'BookShopapp/about.html',date)

def adminresurs(request,root):
    if root:
        if root == 'admin':
            return  render(request, 'BookShopapp/adminresurs.html')
        else :
            return HttpResponseForbidden('<h1>Нет прав</h1>')
    else:
        return HttpResponseBadRequest('<h1>Плохой запрос</h1>')

def hello(request,user):
    return TemplateResponse(request, 'BookShopapp/hello.html',{'user':user})

def info(request):
    list_tex = ['Django','render','django.http','django.http  HttpResponseForbidden, HttpResponseBadRequest','DTL']
    return TemplateResponse(request, 'BookShopapp/info.html',{'list_tex':list_tex})



