from django.db import models

# Create your models here.

class Data(models.Model):
    # 原始数据，用来存储原始的json数据
    original_data = models.CharField(max_length=1000)

    identify_data = models.CharField(max_length=100)


