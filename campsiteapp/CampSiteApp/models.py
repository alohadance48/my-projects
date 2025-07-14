from django.db import models
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import AbstractUser
#from rest_framework.authtoken.models import Token
from django.conf import settings
# Create your models here.


class DateCampModel(models.Model):
    """Модель для дат смен """
    name = models.CharField(max_length=120, unique=True)
    full_name = models.CharField(max_length=120)
    part = models.CharField(max_length=120)
    date = models.DateField()
    price = models.IntegerField()
    places = models.IntegerField(default=1)
    text = models.TextField(blank=True)

    def __str__(self):
        return self.name


class UserModel(AbstractUser):
    """Модель для пользователя от AbstractUser"""
    is_root = models.BooleanField(default=False, unique=False)

    def __str__(self):
        return self.username


class BookingModel(models.Model):
    """Модель для бронирования """
    username = models.CharField(max_length=30)
    id = models.AutoField(primary_key=True)
    status = models.BooleanField(default=False, null=True)
    quantity = models.IntegerField(default=0)
    date_camp = models.ForeignKey(DateCampModel, on_delete=models.CASCADE, related_name='booking')
    surname_parent = models.CharField(max_length=120)
    name_parent = models.CharField(max_length=120)
    patronymic_parent = models.CharField(max_length=120)
    email_parent = models.EmailField()
    number_parent = models.CharField(max_length=120)
    series_passport_parent = models.CharField(max_length=120)
    issued_passport_parent = models.CharField(max_length=120)
    date_of_issue = models.DateField(null=True)
    registration_address_parent = models.CharField(max_length=120)
    surname_child = models.CharField(max_length=120)
    name_child = models.CharField(max_length=120)
    patronymic_child = models.CharField(max_length=120)
    date_of_birth = models.DateField()
    address_child = models.CharField(max_length=120)
    passport_child = models.CharField(max_length=120, null=True)
    issued_passport = models.CharField(max_length=120, null=True)
    date_of_issue_child = models.DateField(null=True)
    series_and_number = models.CharField(max_length=120, null=True)
    comment = models.TextField(null=True)


class ConfirmedBookingsModel(models.Model):
    """Модель для хранения подтвержденных броней."""
    username = models.CharField(max_length=150)
    quantity = models.IntegerField(default=0)


class CommentModel(models.Model):
    """Модель для комментов"""
    username = models.CharField(max_length=4000)
    text = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # Объект ДОЛЖЕН быть привязан к какому-либо datecamp, сами коментарии должны отображаться у указанного date_camp
    stars = models.IntegerField(default=0)

class RecipientModel(models.Model):
    """Модель для рассылки"""
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.email

class DateCampPhotoModel(models.Model):
    """Модель для хранения фоток """
    camp = models.ForeignKey(DateCampModel, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='date_camp_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


from rest_framework.authtoken.models import Token

class ExpiringToken(Token):
   # Модель для drf-token
    class Meta:
        proxy = True

