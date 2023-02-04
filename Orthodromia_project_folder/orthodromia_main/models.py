from django.db import models


# Create your models here.

# Создание Модели для создания формы

class IncomingData(models.Model):
  
   
    p1 = models.CharField(max_length=500,default="")
    p2 = models.CharField(max_length=500)
    NumberOfPoints = models.IntegerField(default="1")
    

