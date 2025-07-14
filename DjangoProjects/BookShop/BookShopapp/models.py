from django.db import models

# Create your models here.
class Users(models.Model):
    user_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    user_password = models.CharField(max_length=50)
    status = models.C
    def __str__(self):
        return self.user_name