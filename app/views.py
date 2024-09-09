from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Recipe, Ingredient, Step
from django.contrib import messages
from django.db.models import Q
from .forms import RecipeForm, IngredientForm, StepForm
from django.contrib.auth import login, logout
from .models import CustomUser

def index(request):
    context = {'user': request.user}
    return render(request, 'index.html', context)

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        new_user = CustomUser(username=username, email=email, password=password)
        new_user.save()
        return HttpResponse('ユーザーの作成に成功しました')
    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return render(request, 'signin.html', {'error_message': 'ユーザーが存在しません。'})

        if user.password == password:
            login(request, user)
            return HttpResponseRedirect('/app/home')
        else:
            return render(request, 'signin.html', {'error_message': 'パスワードが正しくありません。'})
    else:
        return render(request, 'signin.html')

def signout(request):
    logout(request)
    return HttpResponseRedirect('/app')

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
    
def recipe_create(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            # 次へボタンを押したら詳細入力ページへ
            recipe = form.save()
            return redirect('app:detail_create', recipe_id=recipe.id)
        else:
            # 入力していない項目あれば進まない
            template = loader.get_template("app/form.html")
            return HttpResponse(template.render({"form": form}, request))
    else:
        form = RecipeForm()
        template = loader.get_template("app/form.html")
        return HttpResponse(template.render({"form": form}, request))

def detail_create(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)

    if request.method == "POST":
        ingredient_form = IngredientForm(request.POST)
        step_form = StepForm(request.POST, request.FILES)

        if ingredient_form.is_valid() and step_form.is_valid():
            # `Ingredient` の保存
            ingredient = ingredient_form.save(commit=False)
            ingredient.recipe = recipe  # レシピに関連付ける
            ingredient.save()

            # `Step` の保存
            step = step_form.save(commit=False)
            step.recipe = recipe  # レシピに関連付ける
            step.save()

            # 保存後、別のページにリダイレクト（例えば、詳細ページ）
            return redirect('app:detail', post_id=recipe.id)
        else:
            # フォームが無効な場合、エラーメッセージと共にフォームを再表示
            template = loader.get_template("app/form_detail.html")
            return HttpResponse(template.render({
                "ingredient_form": ingredient_form,
                "step_form": step_form,
                "recipe": recipe
            }, request))

    else:
        ingredient_form = IngredientForm()
        step_form = StepForm()
        template = loader.get_template("app/form_detail.html")
        return HttpResponse(template.render({
            "ingredient_form": ingredient_form,
            "step_form": step_form,
            "recipe": recipe
        }, request))