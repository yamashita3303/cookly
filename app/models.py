from django.db import models

#料理全般の情報のテーブル
class Recipe(models.Model):
    #料理タイトル
    cooking_title= models.CharField(max_length=200)
    #料理写真
    cooking_images = models.ImageField(upload_to='recipes/')
    #詳細を開かれた回数
    votes = models.IntegerField(default=0)
    #主菜/副菜/主食/菓子
    genre = models.CharField(max_length=100)
    #料理説明
    detail_text = models.CharField(max_length=200)

#材料のテーブル
class Ingredient(models.Model):
    #class Recipeを継承
    recipe = models.ForeignKey(Recipe, related_name='ingredient', on_delete=models.CASCADE)
    #材料名
    material = models.CharField(max_length=300)
    #分量
    amount = models.CharField(max_length=100)

class Step(models.Model):
    #class Recipeを継承
    recipe = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE)
    #ステップの番号
    step_number = models.IntegerField()
    #作り方の文章
    steps_text = models.CharField(max_length=300)
    #作り方の写真
    steps_images = models.ImageField(upload_to='steps/', blank=True, null=True)
    #作り方の動画
    steps_video = models.FileField(upload_to='videos/', blank=True, null=True)

