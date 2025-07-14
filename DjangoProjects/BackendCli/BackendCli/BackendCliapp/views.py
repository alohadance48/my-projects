from django.shortcuts import render
from django.http import HttpResponse,HttpResponseForbidden,HttpResponseRedirect

# Create your views here.
def index(request):
    return HttpResponse(request)

def about(request,status=None):
    if status:
        if status == 'admin':
            return HttpResponse(request)
        else :
            return HttpResponseForbidden(request)
    else:
        return HttpResponseRedirect('.')

def contact(request):
    return HttpResponse(request)

