from django.http import HttpResponse
from django.template import loader
from .models import Recipe, Ingredient, Step

def index(request):
    template = loader.get_template("app/index.html")
    return HttpResponse(template.render({}, request))

def recipe(request):
    recipes = Recipe.objects.all()
    #recipesのlistになっている。
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