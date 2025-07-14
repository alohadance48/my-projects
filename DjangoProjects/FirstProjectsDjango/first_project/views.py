from django.shortcuts import render
from django.http import HttpResponse,HttpResponseForbidden,HttpResponseBadRequest



# Create your views here.

def index(request):
    '''Главная страница моего сайта'''
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def admin_resurs(request,root=None):
    if root:
        if root == 'admin':
            return HttpResponse('<h1>Admin</h1>')
        else :
            return HttpResponseForbidden('<h1>Нет прав</h1>')
    else :
        return  HttpResponseBadRequest('<h1>Ошибка</h1>')




