from django.db import models

# Create your models here.
class Autorisation(models.Model):
    username = models.CharField(max_length=60)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=40)
    def __str__(self):
        return self.username