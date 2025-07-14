from django import forms
from django.db.models.fields import EmailField


class UserForm(forms.Form):
    name = forms.CharField()
    age = forms.IntegerField()
    Json = forms.JSONField()
    basket = forms.BooleanField(label='Basket')
    ling = forms.ChoiceField(label='Выбери язык:',choices=((1,'Английский'),(2,'Немецкий'),(3,'Французкий')))
    files = forms.FilePathField(label='Файл:',path='/home/vladosl',allow_files=True,allow_folders=True)
    time = forms.DateTimeField(label='Введите время:')
    ip = forms.GenericIPAddressField(label='IP:')
    img = forms.ImageField(label='Изображение:')
    choice = forms.NullBooleanField(label='Ты гей?')
    info = forms.ComboField(label='Введите данные :',fields=[
        forms.CharField(label='test'),
        forms.CharField(label='test2'),
    ])
    comment = forms.CharField(label='test',widget=forms.Textarea,initial='test')
    field_order = [
        'name',
        'age',
        'json',
        'basket',
        'ling',
        'files',
        'info'
    ]
