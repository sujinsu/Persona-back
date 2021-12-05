from django.db import models

# Create your models here.
class BalanceGame(models.Model):
    title=models.CharField(max_length=150)
    option1=models.CharField(max_length=150)
    img1=models.CharField(max_length=200)
    vote1=models.IntegerField()
    option2=models.CharField(max_length=150)
    img2=models.CharField(max_length=200)
    vote2=models.IntegerField()
    option3=models.CharField(max_length=150)
    img3=models.CharField(max_length=200)
    vote3=models.IntegerField()