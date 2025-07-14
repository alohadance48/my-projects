from django import forms


class Staff(forms.Form):
    name = forms.CharField(label='Введите ваш имя',max_length=15,min_length=5)
    title = forms.CharField(label='Введите вашу должность:',max_length=15,min_length=5)
    password = forms.CharField(widget=forms.PasswordInput(),label='Введите пароль от учетной записи:',max_length=15,min_length=5)
    email = forms.EmailField(label='Введите ваш e-mail:',max_length=15,min_length=5)

class Logout(forms.Form):
    name = forms.CharField(label='Введите ваше имя:',max_length=15,min_length=5)
    password = forms.CharField(label='Введите пароль:',widget=forms.PasswordInput(),max_length=15,min_length=5)
    email = forms.EmailField(label='Введите e-mail:',max_length=15,min_length=5)

class Address(forms.Form):
    address = forms.CharField(label='Адрес:',max_length=40,min_length=15)
    email = forms.EmailField(label='Введите  e-mail:',max_length=15,min_length=5)
    name = forms.CharField(label='Введите свое имя :',max_length=15,min_length=5)
    time = forms.DateField(label='Введите время:',widget=forms.TimeInput())









