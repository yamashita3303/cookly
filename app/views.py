from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.views import View
from .models import Recipe, Ingredient, Step, Favorite
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RecipeForm, IngredientForm, StepForm, CommentForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser


def index(request):
    context = {'user': request.user}
    return render(request, 'index.html', context)

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user_icon = request.FILES.get('user_icon')  # アイコンファイルを取得
        print(user_icon)
        new_user = CustomUser(
            first_name=first_name, 
            last_name=last_name, 
            username=username, 
            email=email,
            user_icon=user_icon  # アイコンを保存
        )
        new_user.set_password(password)  # パスワードのハッシュ化
        new_user.save()
        
        # signup_success.htmlでアラートを表示し、リダイレクトさせる
        return render(request, 'signup_success.html', {'message': 'ユーザーの作成に成功しました'})
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

        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/home/')
        else:
            return render(request, 'signin.html', {'error_message': 'パスワードが正しくありません。'})
    else:
        return render(request, 'signin.html')

# ログアウトビュー
@login_required
def signout(request):
    logout(request)
    messages.success(request, "ログアウトしました。")
    return redirect('app:index')

# レシピ一覧ページ(home.html)
def recipe(request):
    # GETリクエストからジャンルを取得
    selected_genre = request.GET.get('genre')

    # 人気料理、最新の料理の上位10個だけ取得
    # 評価の星はもうちょっと考えたいからいったん閲覧数順で並び替え
    popular_recipes = Recipe.objects.all().order_by('-vote')[:10]
    latest_recipes = Recipe.objects.all().order_by('-created_at')[:10]

    # ジャンルでのフィルタリング
    if selected_genre:
        # 選択されたジャンルでフィルターをかける
        all_recipes = Recipe.objects.filter(genre=selected_genre)
    else:
        # すべてのレシピを取得
        all_recipes = Recipe.objects.all()

    # リストに似たオブジェクトになっている。
    context = {
        'popular_recipes': popular_recipes,
        'latest_recipes': latest_recipes,
        'all_recipes': all_recipes,
        'selected_genre': selected_genre,
    }
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
    
    is_favorited = False
    if request.user.is_authenticated:
        from app.models import Favorite  # 追加
        is_favorited = Favorite.objects.filter(user=request.user, item=recipes).exists()


    context = {
        "recipe_chose": recipes,
        "ingredient_text": ingredient_text,
        'steps': steps,
        "comments": comments,
        "user": recipes.user,
        "is_favorited": is_favorited, 
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
    
    return render(request, 'app/home.html', {'search_recipes': search_recipes})

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
            comment.user = request.user  # ログインユーザーをセット
            comment.recipe = recipe

        # 星評価を保存するための処理
            rating_value = request.POST.get('rating')  # POSTデータから 'rating' を取得


            if rating_value:
                try:
                    rating_value = int(rating_value)  # 'rating' の値を整数に変換
                    comment.rating = rating_value  # コメントに評価を紐付ける
                    
                except ValueError:
                    
                    # 変換に失敗した場合の処理（例: 'rating' が不正な場合）
                    pass

            comment.save()
            return redirect('app:detail', post_id=recipe.id)
        else:
            context = {
                'form': form,
                'recipe': recipe
            }
            return render(request, 'app/comment.html', context)

# 料理の基本情報(タイトル、画像など)を追加するフォーム(form.html) 
class RecipeCreateView(LoginRequiredMixin, View):
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
        print(request.POST)
        print(request.FILES)
        # インスタンスの作成
        recipe_form = RecipeForm(request.POST, request.FILES)
        ingredient_form = IngredientForm(request.POST)

        materials = request.POST.getlist('material')
        amounts = request.POST.getlist('amount')
        # ステップ情報を取得
        step_numbers = request.POST.getlist('step_number')
        step_texts = request.POST.getlist('step_text')
        step_videos = request.FILES.getlist('step_video')

        step_form = StepForm()

        # フォームが有効かチェック
        if recipe_form.is_valid() and ingredient_form.is_valid():
            # 料理情報を保存
            recipe = recipe_form.save(commit=False)
            recipe.user = request.user  # ログインしているユーザーを設定
            recipe.save()

            # 材料情報を保存
            for material, amount in zip(materials, amounts):
                ingredient = Ingredient(
                    recipe=recipe,
                    material=material,
                    amount=amount
                )
                ingredient.save()

            # ステップ情報を保存
            for i in range(len(step_texts)):
                step_text = step_texts[i]
                step_image = request.FILES.get(f'step_image_{i+1}', None)
                step_video = step_videos[i] if i < len(step_videos) else None

                step = Step(
                    recipe=recipe,
                    step_number=i + 1,
                    step_text=step_text,
                    step_image=step_image if step_image else None,
                    step_video=step_video if step_video else None
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

def recipe_edit(request, post_id):
    # 指定されたIDのレシピを取得
    recipe = get_object_or_404(Recipe, id=post_id)

    if request.method == "POST":
        # フォームにPOSTデータをバインド
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            # フォームが有効な場合、レシピを保存
            form.save()
            messages.success(request, "レシピが正常に更新されました。")
            return redirect('app:detail', post_id=recipe.id)  # 編集後に詳細ページにリダイレクト
    else:
        # GETリクエストの場合、既存のレシピデータをフォームに渡す
        form = RecipeForm(instance=recipe)

    return render(request, 'app/recipe_edit.html', {'form': form, 'recipe': recipe})

#レシピの消去
def recipe_delete(request, post_id):
    # 指定されたIDのレシピを取得
    recipes = Recipe.objects.get(id=post_id)
    #メッセージ表示
    messages.success(request, "消去しました。")
    recipes.delete()
    return redirect("/home/")

@login_required
def mypage(request):
    user = request.user  # ログイン中のユーザーを取得
    recipes = user.recipe_set.all()  # ユーザーが投稿した全ての料理を取得
    
    favorite_recipes = Favorite.objects.filter(user=user).select_related('item')

    return render(request, 'app/mypage.html', {
        'user': user,
        'recipes': recipes,
        'favorite_recipes': favorite_recipes,
    })

# classをview関数に変換
comments = CommentCreateView.as_view()
recipe_create = RecipeCreateView.as_view()

@login_required
def toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, item=recipe)
    if not created:
        favorite.delete()  # 既にお気に入りに登録されている場合は解除
    return redirect("app:detail", post_id=recipe.id)


