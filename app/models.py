from django.db import models

#料理全般の情報のテーブル
class Recipe(models.Model):
    #料理タイトル
    recipe_title = models.CharField(max_length=200, verbose_name="料理タイトル")
    #料理写真
    recipe_image = models.ImageField(upload_to='recipes/', verbose_name="料理写真")
    #詳細を開かれた回数
    vote = models.IntegerField(default=0, verbose_name="閲覧回数")
    #料理説明
    detail_text = models.TextField(max_length=200, verbose_name="料理説明")
    #主菜/副菜/主食/菓子
    class Genre(models.TextChoices):
        MAIN_DISH = 'main', '主菜'
        SIDE_DISH = 'side', '副菜'
        MAIN_COURSE = 'course', '主食'
        DESSERT = 'dessert', '菓子'
    genre = models.CharField(max_length=10, choices=Genre.choices, verbose_name="ジャンル")
    #作成日
    created_at = models.DateTimeField(auto_now_add=True)
    #更新日
    updated_at = models.DateField(verbose_name="更新日", auto_now=True)

#材料のテーブル
class Ingredient(models.Model):
    #class Recipeを継承
    recipe = models.ForeignKey(Recipe, related_name='ingredient', on_delete=models.CASCADE, verbose_name="class Recipeを継承")
    #材料名
    material = models.CharField(max_length=100, verbose_name="材料名")
    #分量
    amount = models.CharField(max_length=100, verbose_name="分量")

class Step(models.Model):
    #class Recipeを継承
    recipe = models.ForeignKey(Recipe, related_name='step', on_delete=models.CASCADE)
    #ステップの番号
    step_number = models.PositiveIntegerField(verbose_name="ステップ番号")
    #作り方の文章
    step_text = models.CharField(max_length=300, verbose_name="作り方文章")
    #作り方の写真   blank=True, null=Trueは任意で登録できるように
    step_image = models.ImageField(upload_to='steps/', blank=True, null=True, verbose_name="作り方の写真")
    #作り方の動画   blank=True, null=Trueは任意で登録できるように
    step_video = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name="作り方の動画")


#コメント機能
class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='comment', on_delete=models.CASCADE)

    #コメントしたユーザー名
    #日時
    created_at = models.DateTimeField(auto_now_add=True)
    #コメント
    comment = models.TextField(max_length=200)
    #評価
    class Review(models.TextChoices):
        ONE_STAR = 'one', '★'
        TWO_STAR = 'two', '★★'
        THREE_STAR = 'three', '★★★'
        FOUR_STAR = 'four', '★★★★'
        FIVE_STAR = 'five', '★★★★★'
    review = models.CharField(max_length=10, choices=Review.choices, verbose_name="レビュー")