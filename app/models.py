from django.db import models

class Cooking(models.Model):
    cooking_title= models.CharField(max_length=200)
    cooking_images = models.ImageField(upload_to='')

class Detail(models.Model):
    #class Cookingを継承
    cooking = models.ForeignKey(Cooking, on_delete=models.CASCADE)
    #主菜/副菜/主食/菓子
    genre = models.CharField(max_length=100)
    #材料
    material = models.CharField(max_length=300)
    #作り方の文章
    steps_text = models.CharField(max_length=300)
    #作り方の写真
    steps_images = models.ImageField(upload_to='')
    
    #作り方の動画
    #steps_movies = models.ImageField(upload_to='')
    
    #料理説明
    detail_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

