from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.views import View
from .models import Recipe, Ingredient, Step, Comment
from .forms import RecipeForm, IngredientForm, StepForm, CommentForm
from django.contrib.auth import login, logout
from .models import CustomUser
# 今は使ってない
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
    # ステップデータを取得
    steps = recipes.step.all()
    # コメントを取得
    comments = recipes.comment.all()

    # 閲覧数を1増やして保存
    recipes.vote += 1
    recipes.save()

    context = {
        "recipe_chose": recipes,
        "ingredient_text": ingredient_text,
        'steps': steps,
        "comments": comments,
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

class CommentCreateView(View):
    # GETリクエストの処理
    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        form = CommentForm()
        context = {
            'form': form,
            'recipe': recipe
        }
        return render(request, 'app/comment.html', context)

    # POSTリクエストの処理
    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.save()
            return redirect('app:detail', post_id=recipe.id)
        else:
            context = {
                'form': form,
                'recipe': recipe
            }
            return render(request, 'app/comment.html', context)

# 料理の基本情報(タイトル、画像など)を追加するフォーム(form.html) 
class RecipeCreateView(View):
    # GETリクエストの処理
    def get(self, request):
        # インスタンスの作成
        recipe_form = RecipeForm()
        ingredient_form = IngredientForm()
        step_form = StepForm()

        context = {
            'form': recipe_form,
            'ingredient_form': ingredient_form,
            'step_form': step_form,
        }
        return render(request, 'app/form.html', context)

    # POSTリクエストの処理
    def post(self, request):
        # インスタンスの作成
        recipe_form = RecipeForm(request.POST, request.FILES)
        ingredient_form = IngredientForm(request.POST)

        # ステップ情報を取得
        step_numbers = request.POST.getlist('step_number')
        step_texts = request.POST.getlist('step_text')
        step_images = request.FILES.getlist('step_image')
        step_videos = request.FILES.getlist('step_video')

        step_form = StepForm()

        # フォームが有効かチェック
        if recipe_form.is_valid() and ingredient_form.is_valid():
            # 料理情報を保存
            recipe = recipe_form.save()

            # 材料情報を保存
            ingredient = ingredient_form.save(commit=False)
            ingredient.recipe = recipe
            ingredient.save()

            # ステップ情報を保存
            for i, (step_number, step_text) in enumerate(zip(step_numbers, step_texts)):
                step_image = step_images[i] if i < len(step_images) else None
                step_video = step_videos[i] if i < len(step_videos) else None
                step = Step(
                    recipe=recipe,
                    step_number=step_number,
                    step_text=step_text,
                    step_image=step_image,
                    step_video=step_video
                )
                step.save()

            return redirect('app:recipe')

        # フォームが無効なら再表示
        context = {
            'form': recipe_form,
            'ingredient_form': ingredient_form,
            'step_form': step_form,
        }
        return render(request, 'app/form.html', context)

# classをview関数に変換
comments = CommentCreateView.as_view()
recipe_create = RecipeCreateView.as_view()
