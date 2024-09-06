from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.views import View
from .models import Recipe, Ingredient, Step
from .forms import RecipeForm, IngredientForm, StepForm

# 今は使ってない
def index(request):
    # render()にはrequest, htmlファイル名, 渡したいデータ(辞書型)を入れる
    return render(request, "app/index.html")

# レシピ一覧ページ(home.html)
def recipe(request):
    # GETリクエストからジャンルを取得
    selected_genre = request.GET.get('genre')

    # ジャンルでのフィルタリングと同時に閲覧数の多い順に並べる
    if selected_genre:
        # 選択されたジャンルでフィルターをかける
        recipes = Recipe.objects.filter(genre=selected_genre).order_by('-vote')
    else:
        # すべてのレシピを取得
        recipes = Recipe.objects.all().order_by('-vote')

    # リストに似たオブジェクトになっている。
    context = {'recipe_all': recipes, 'selected_genre': selected_genre}
    return render(request, "app/home.html", context)

# レシピの詳細ページ(recipe.html)
def detail(request, post_id):
    # 指定されたIDのレシピを取得
    recipes = Recipe.objects.get(id=post_id)
    # レシピに関連する材料の取得
    ingredient_text = recipes.ingredient.all()

    # 閲覧数を1増やして保存
    recipes.vote += 1
    recipes.save()

    context = {
        "recipe_chose": recipes,
        "ingredient_text": ingredient_text,
    }
    return render(request, "app/recipe.html", context)

# レシピ検索ページ(searchrecipes.html)
def search_recipes(request):
    # Recipeモデルの全てのインスタンスを取得
    recipes = Recipe.objects.all()

    # 検索機能の処理
    # 入力したキーワードが含まれる料理名でフィルタリング
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


# 料理の基本情報(タイトル、画像など)を追加するフォーム(form.html) 
class RecipeCreateView(View):
    # GETリクエストの処理
    def get(self, request):
        # フォームの表示
        form = RecipeForm()
        return render(request, 'app/form.html', {'form': form})

    # POSTリクエストの処理
    def post(self, request):
        # 送信されたデータをいったんformに入れる
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            # 必須項目が埋まっていたら保存後、詳細入力ページへ
            recipe = form.save()
            return redirect('app:detail_create', recipe_id=recipe.id)
        
        # 必須項目が埋まってなければ再度フォームを表示
        return render(request, 'app/form.html', {'form': form})


# レシピの詳細を記入するフォーム(form_detail.html)
class DetailCreateView(View):
    # GETリクエストの処理
    def get(self, request, recipe_id):
        return self.render_form(request, recipe_id)

    # POSTリクエストの処理
    def post(self, request, recipe_id):
        # 対象のレシピが存在しなければエラーを返す
        recipe = get_object_or_404(Recipe, id=recipe_id)
        # フォームの表示
        ingredient_form = IngredientForm(request.POST)
        step_form = StepForm(request.POST, request.FILES)
        
        # それぞれのフォームが有効ならば保存後、レシピ一覧ページへ
        if ingredient_form.is_valid() and step_form.is_valid():
            self.save_forms(ingredient_form, step_form, recipe)
            return redirect('app:recipe')
        
        # フォームが無効なら再度フォームを表示
        return self.render_form(request, recipe_id, ingredient_form, step_form)


    # get()から呼び出されるメソッド
    # フォームを表示する
    def render_form(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ingredient_form = IngredientForm()
        step_form = StepForm()
        context = {
            'ingredient_form': ingredient_form,
            'step_form': step_form,
            'recipe': recipe,
        }
        return render(request, 'app/form_detail.html', context)

    # post()から呼び出されるメソッド
    # 材料と手順を保存する
    def save_forms(self, ingredient_form, step_form, recipe):
        # 材料、ステップの保存
        ingredient = ingredient_form.save(commit=False)
        ingredient.recipe = recipe
        ingredient.save()

        step = step_form.save(commit=False)
        step.recipe = recipe
        step.save()

# classをview関数に変換
recipe_create = RecipeCreateView.as_view()
detail_create = DetailCreateView.as_view()
