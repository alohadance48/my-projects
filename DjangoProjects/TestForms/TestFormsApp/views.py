from django.shortcuts import render
from TestFormsApp.forms import UserForm

# Create your views here.
def index(request):
    my_form = UserForm()
    context = {'my_form': my_form}
    return render(request, 'TestFormsApp/index.html', context)

def my_form(request):
    my_form = UserForm(file_order=['json','name'])
    context = {'my_form': my_form}
    return render(request, 'TestFormsApp/my_form.html',context)

def test(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            output = "<2>test:</h2><h1>{0}</h1>".format(name)
        else:
            return render(request,'<h1>Error</h1>')
    else :
        user_form = UserForm()