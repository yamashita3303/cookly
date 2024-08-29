from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.views import View
from .models import Recipe, Ingredient, Step
from .forms import RecipeForm, IngredientForm, StepForm

def index(request):
    # render()にはrequest, htmlファイル名, 渡したいデータ(辞書型)を入れる
    return render(request, "app/index.html")

def recipe(request):
    selected_genre = request.GET.get('genre')

    if selected_genre:
        # 選択されたジャンルでフィルターをかける
        recipes = Recipe.objects.filter(genre=selected_genre).order_by('-vote')
    else:
        # すべてのレシピを取得
        recipes = Recipe.objects.all().order_by('-vote')

    # リストに似たオブジェクトになっている。
    context = {'recipe_all': recipes, 'selected_genre': selected_genre}
    return render(request, "app/home.html", context)

def detail(request, post_id):
    recipes = Recipe.objects.get(id=post_id)
    ingredient_text = recipes.ingredient.all()

    recipes.vote += 1
    recipes.save()

    context = {
        "recipe_chose": recipes,
        "ingredient_text": ingredient_text,
    }
    return render(request, "app/recipe.html", context)

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
    else:
        # 検索キーワードがない場合
        messages.error(request, '検索キーワードが指定されていません。')
        search_recipes = recipes
    
    return render(request, 'app/searchrecipes.html', {'search_recipes': search_recipes})

# 料理の見出し記入 
class RecipeCreateView(View):
    def get(self, request):
        # フォームの表示
        form = RecipeForm()
        return render(request, 'app/form.html', {'form': form})

    def post(self, request):
        # データの保存
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            # 必須項目が埋まっていたら保存後、ホームへ戻る
            recipe = form.save()
            return redirect('app:detail_create', recipe_id=recipe.id)
        return render(request, 'app/form.html', {'form': form})

# レシピの詳細記入
class DetailCreateView(View):
    def get(self, request, recipe_id):
        return self.render_form(request, recipe_id)

    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ingredient_form = IngredientForm(request.POST)
        step_form = StepForm(request.POST, request.FILES)
        
        if ingredient_form.is_valid() and step_form.is_valid():
            self.save_forms(ingredient_form, step_form, recipe)
            return redirect('app:recipe')
        
        return self.render_form(request, recipe_id, ingredient_form, step_form)

    def save_forms(self, ingredient_form, step_form, recipe):
        # 材料、ステップの保存
        ingredient = ingredient_form.save(commit=False)
        ingredient.recipe = recipe
        ingredient.save()

        step = step_form.save(commit=False)
        step.recipe = recipe
        step.save()

    def render_form(self, request, recipe_id):
        # フォームの表示
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ingredient_form = IngredientForm()
        step_form = StepForm()
        context = {
            'ingredient_form': ingredient_form,
            'step_form': step_form,
            'recipe': recipe,
        }
        return render(request, 'app/form_detail.html', context)

# classをview関数に変換
recipe_create = RecipeCreateView.as_view()
detail_create = DetailCreateView.as_view()
