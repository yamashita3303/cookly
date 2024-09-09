from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Recipe, Ingredient, Step
from django.contrib import messages
from django.db.models import Q

def index(request):
    template = loader.get_template("app/index.html")
    return HttpResponse(template.render({}, request))

def recipe(request):
    #インスタンス化
    recipes = Recipe.objects.all()
    #リストに似たオブジェクトになっている。
    context = {'recipe_all': recipes}
    template = loader.get_template("app/home.html")
    return HttpResponse(template.render(context, request))

def detail(request, post_id):
    recipes = Recipe.objects.get(id=post_id)
    ingredient_text = recipes.ingredient.all()
    context = {
        "recipe_chose": recipes,
        "ingredient_text": ingredient_text,
    }
    template = loader.get_template("app/recipe.html")
    return HttpResponse(template.render(context, request))

def search_recipes(request):
    # Recipeモデルの全てのインスタンスを取得
    recipes = Recipe.objects.all()

    # 検索機能の処理
    keyword = request.GET.get('keyword')
    if keyword:
        search_recipes = recipes.filter(
            Q(recipe_title__icontains=keyword)
        )
        messages.success(request, '[{}]の検索結果'.format(keyword))
        return render(request, 'app/searchrecipes.html', {'search_recipes': search_recipes})
    else:
        # 検索キーワードがない場合
        messages.error(request, '検索キーワードが指定されていません。')
        return render(request, 'app/searchrecipes.html', {'search_recipes': recipes})