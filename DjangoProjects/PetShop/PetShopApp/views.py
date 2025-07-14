from django.shortcuts import render
from django.template.response import  TemplateResponse
from django.http import HttpResponse,HttpResponseForbidden
from django.shortcuts import redirect
from PetShopApp.forms import *



# Create your views here.
def index (request):
    return TemplateResponse(request, 'PetShopApp/index.html')

def about(request):
    return TemplateResponse(request, 'PetShopApp/about.html')

def contact(request):
        return TemplateResponse(request, 'PetShopApp/contact.html')

def staff (request,status=None):
    if status:
        if status == 'staff':
            return TemplateResponse(request, 'PetShopApp/staff.html')
        else :
            return HttpResponseForbidden('<h1>Forbidden</h1>')
    elif status is None:
        return redirect('index',permanent=True)


def private(request,status):
    if status:
        if status == 'private':
            return TemplateResponse(request, 'PetShopApp/private.html')
        else:
            HttpResponseForbidden('<h1>Forbidden</h1>')
    else :
        return redirect('index',permanent=True)

def logout(request):
    my_form = {'my_form': Staff()}
    return TemplateResponse(request, 'PetShopApp/logout.html', my_form)

def login(request):
    my_form = {'my_form': Logout()}
    return TemplateResponse(request, 'PetShopApp/login.html', my_form)

def address(request):
    my_form = {'my_form': Address()}
    return TemplateResponse(request, 'PetShopApp/address.html', my_form)



