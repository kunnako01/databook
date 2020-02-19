from django.db import models

class Post1(models.Model):
    name = models.CharField(max_length = 200)
    des = models.TextField() 
