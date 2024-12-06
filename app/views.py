from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Avg
from django.views import View
from .models import Recipe, Ingredient, Step, Favorite, Comment, Allergy, Inventorylog
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from .forms import RecipeForm, IngredientForm, StepForm, CommentForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser, Follow
import datetime, calendar, openai, os
from datetime import datetime
from flaretool.holiday import JapaneseHolidaysOnline
from dotenv import load_dotenv
from collections import defaultdict
from django.http import JsonResponse
from django.utils.timezone import now, make_aware

def index(request):
    context = {'user': request.user}
    return render(request, 'index.html', context)

def signup(request):
    allergy_object = Allergy.objects.all()
    context = {"allergy_object":allergy_object}
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        allergy_list = request.POST.getlist('allergy')
        allergy_string = ','.join(allergy_list) # 要素を区別できるようにカンマで区切る
        user_icon = request.FILES.get('user_icon')  # アイコンファイルを取得
        new_user = CustomUser(
            username=username, 
            email=email,
            user_icon=user_icon,
            allergy=allergy_string
        )
        new_user.set_password(password)  # パスワードのハッシュ化
        new_user.save()

        # 新規登録後はその情報でログイン(デバッグ用)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            return HttpResponseRedirect('/home/')
        
        # signup_success.htmlでアラートを表示し、リダイレクトさせる
        return render(request, 'signup_success.html', {'message': 'ユーザーの作成に成功しました'})
    else:
        return render(request, 'signup.html', context)

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

def allergy(request):
    allergies = Allergy.objects.all()
    if request.method == 'POST':
        delete_id = request.POST.get('delete_id')
        allergy_id = request.POST.get('allergy_id')
        allergy_name = request.POST.get('allergy_name')
        allergy_image = request.FILES.get('allergy_image')
        if allergy_image:
            print(f"Image uploaded: {allergy_image.name}")
        else:
            print("No image uploaded")

        if delete_id:
            allergy = get_object_or_404(Allergy, id=delete_id)
            allergy.delete()
        elif allergy_id:
            # 追加のidフィールドは隠しているためidに何かが入力されていれば編集
            allergy = get_object_or_404(Allergy, id=allergy_id)
            allergy.allergy_name = allergy_name
            if allergy_image:
                allergy.allergy_image = allergy_image
            allergy.save()
        else:
            # idに何も入力されてなければ追加
            if allergy_name:
                Allergy.objects.create(
                    allergy_name=allergy_name,
                    allergy_image=allergy_image
                )
        return redirect('app:allergy')
    
    return render(request, 'app/allergy.html', {'allergies': allergies})

# レシピ一覧ページ(home.html)
def recipe(request):
    # GETリクエストからジャンルを取得
    selected_genre = request.GET.get('genre')
    min_rating = request.GET.get('min_rating')  # 最低評価
    exclude_allergies = request.GET.get('exclude_allergies') == "on"

    # 人気料理、最新の料理の上位3個だけ取得
    popular_recipes = Recipe.objects.annotate(average_rating=Avg('comment__rating')).order_by('-average_rating')[:3]
    latest_recipes = Recipe.objects.all().annotate(average_rating=Avg('comment__rating')).order_by('-created_at')[:3]

    # ジャンルでのフィルタリング
    if selected_genre:
        # 選択されたジャンルでフィルターをかける
        all_recipes = Recipe.objects.filter(genre=selected_genre).annotate(average_rating=Avg('comment__rating'))
    else:
        # すべてのレシピを取得
        all_recipes = Recipe.objects.all().annotate(average_rating=Avg('comment__rating'))

    # 最低評価でフィルタリング
    if min_rating:
        all_recipes = [recipe for recipe in all_recipes if recipe.average_rating and recipe.average_rating >= float(min_rating)]

    # ログイン中ならばアレルギーを取得する
    if request.user.is_authenticated:  # ユーザーがログインしている場合
        if request.user.allergy == "なし":
            allergies = []
        else:
            allergies = request.user.allergy.split(',')
    else:  # 未ログインのユーザーの場合
        allergies = []

    # 各レシピに対してアレルギー食材を含むかどうかをチェック
    def check_allergy_flag(recipes):
        for recipe in recipes:
            # アレルギー食材を含む場合、allergy_flagをTrueに設定
            recipe.allergy_flag = Ingredient.objects.filter(recipe=recipe, material__in=allergies).exists()
        return recipes

    # 人気レシピ、最新レシピ、全レシピにアレルギー判定を追加
    popular_recipes = check_allergy_flag(popular_recipes)
    latest_recipes = check_allergy_flag(latest_recipes)
    all_recipes = check_allergy_flag(all_recipes)

    # アレルギーを含むレシピを除外
    if exclude_allergies:
        all_recipes = [recipe for recipe in all_recipes if not recipe.allergy_flag]

    # リストに似たオブジェクトになっている。
    context = {
        'popular_recipes': popular_recipes,
        'latest_recipes': latest_recipes,
        'all_recipes': all_recipes,
        'selected_genre': selected_genre,
        'min_rating': min_rating,
        'exclude_allergies': exclude_allergies,
        'allergies': allergies,
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
    is_folloing = False
    if request.user.is_authenticated:
        from app.models import Favorite  # 追加
        is_favorited = Favorite.objects.filter(user=request.user, item=recipes).exists()
        is_folloing = Follow.objects.filter(follower=request.user, followed=recipes.user).exists()

    context = {
        "recipe_chose": recipes,
        "ingredient_text": ingredient_text,
        'steps': steps,
        "comments": comments,
        "user": recipes.user,
        "is_favorited": is_favorited, 
        "is_following": is_folloing,
    }
    return render(request, "app/recipe.html", context)

# レシピ検索ページ(searchrecipes.html)
def search_recipes(request):
    # Recipeモデルの全てのインスタンスを取得
    recipes = Recipe.objects.all().annotate(average_rating=Avg('comment__rating'))

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
    recipes = user.recipe_set.all().annotate(average_rating=Avg('comment__rating'))  # ユーザーが投稿した全ての料理を取得
    if user.allergy == "なし":
        allergies = []
    else:
        allergies = user.allergy.split(',')
    
    favorite_recipes = Favorite.objects.filter(user=user).select_related('item')
    followed_authors = Follow.objects.filter(follower=user).select_related('followed')  # フォロー中の投稿者
    return render(request, 'app/mypage.html', {
        'user': user,
        'recipes': recipes,
        'allergies': allergies,
        'favorite_recipes': favorite_recipes,
        'followed_authors': followed_authors,
    })
    return render(request, 'app/mypage.html', context)

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

@login_required
def toggle_follow(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)
    if request.user == target_user:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/')) # 自分自身をフォローできないようにリダイレクト

    follow_obj, created = Follow.objects.get_or_create(follower=request.user, followed=target_user)
    if not created:
        follow_obj.delete()  # 既にフォローしていた場合は削除
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def author_page(request, user_id):
    author = get_object_or_404(CustomUser, id=user_id)
    recipes = Recipe.objects.filter(user=author).annotate(average_rating=Avg('comment__rating'))  # 投稿者のレシピを取得

    context = {
        'author': author,
        'recipes': recipes,
    }
    return render(request, 'app/author_page.html', context)


@login_required
def reply_to_comment(request, recipe_id, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                user=request.user,
                recipe=recipe,
                parent=parent_comment,
                content=content
            )
        return redirect('app:detail', post_id=recipe_id)

    return render(request, 'app/reply.html', {
        'parent_comment': parent_comment,
        'recipe': recipe,
    })

#星評価計算
def home(request):
    # レシピリストと平均評価を取得
    recipes = Recipe.objects.all().annotate(average_rating=Avg('comments__rating__value'))

    context = {
        'recipes': recipes,
    }
    return render(request, 'app/home.html', context)

def recipe_calendar(request):
    current_user = request.user
    print("user = ",current_user)
    holiday_name = []
    holiday_date = []
    inventory_log_name = []
    inventory_log_date = []
    if request.method == 'POST':
        yearmonth = request.POST.get('yearmonth')
        year = yearmonth[0]+yearmonth[1]+yearmonth[2]+yearmonth[3]
        month = yearmonth[5:]

        inventory_log = Inventorylog.objects.filter(user=current_user, expiration_date__year=year, expiration_date__month=month)
        for inventory_log in inventory_log:
            inventory_log_name.append(inventory_log.ingredient_name)
            inventory_log_date.append(inventory_log.expiration_date.day)
        print("inventory_log_name = {}".format(inventory_log_name))
        print("inventory_log_date = {}".format(inventory_log_date))
        calendar_month = calendar.monthcalendar(int(year),int(month))
        holidays = JapaneseHolidaysOnline()
        if len(month) == 1:
            month = "0" + month
        holiday_list = holidays.get_holidays(year + month)
        for holiday in holiday_list:
            name, date = holiday
            holiday_name.append(name)
            holiday_date.append(date.day)
        context = {
            "year":year,
            "month":month,
            "yearmonth":yearmonth,
            "calendar_month":calendar_month,
            "holiday_name":holiday_name,
            "holiday_date":holiday_date,
            "inventory_log_name":inventory_log_name,
            "inventory_log_date":inventory_log_date,
                   }
    else:
        currentDateTime = datetime.now()
        date = currentDateTime.date()
        year = date.strftime("%Y")
        month = date.strftime("%m")
        
        inventory_log = Inventorylog.objects.filter(user=current_user, expiration_date__year=year, expiration_date__month=month)
        for inventory_log in inventory_log:
            inventory_log_name.append(inventory_log.ingredient_name)
            inventory_log_date.append(inventory_log.expiration_date.day)
        print("inventory_log_name = {}".format(inventory_log_name))
        print("inventory_log_date = {}".format(inventory_log_date))

        calendar_month = calendar.monthcalendar(int(year), int(month))
        holidays = JapaneseHolidaysOnline()
        if len(month) == 1:
            month = "0" + month
        holiday_list = holidays.get_holidays(year + month)
        for holiday in holiday_list:
            name, date = holiday
            holiday_name.append(name)
            holiday_date.append(date.day)
        print("holiday_name = {}".format(holiday_name))
        print("holiday_date = {}".format(holiday_date))
        context = {
            "year":year,
            "month":month,
            "calendar_month":calendar_month,
            "holiday_name":holiday_name,
            "holiday_date":holiday_date,
            "inventory_log_name":inventory_log_name,
            "inventory_log_date":inventory_log_date,
        }
    return render(request, 'app/calendar.html', context)

# .env ファイルを読み込む
load_dotenv()

# .env から OPENAI_API_KEY を取得
openai.api_key = os.getenv('OPENAI_API_KEY')

def ingredients_management(request):
    user = request.user
    if request.method == 'POST':
        ingredient_name = request.POST.get('ingredient_name')
        expiration_date = request.POST.get('expiration_date')
        
        print("ingredient_name = {}".format(ingredient_name))
        print("expiration_date = {}".format(expiration_date))

        expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d')
        expiration_date = make_aware(expiration_date)
        
        if expiration_date >= now().replace(hour=0, minute=0, second=0, microsecond=0):
            storage_method = gpt_search(ingredient_name)
            print("storage_method = {}".format(storage_method))
            # 保存処理
            inventorylog = Inventorylog(
                user=user,
                ingredient_name=ingredient_name,
                expiration_date=expiration_date,
                storage_method=storage_method
            )
            inventorylog.save()

            return render(request, 'app/ingredients_management.html', {"message": "保存が完了しました！"})

        else:
            print("-------")
            return render(request, 'app/ingredients_management.html', {"message": "現在の日付より前は登録できません"})
    else:
        return render(request, "app/ingredients_management.html")

def gpt_search(text):
    try:
        # プロンプトを作成
        text += "の保存方法を70字程度で"
        print(f"プロンプト = {text}")
        
        # ChatGPTにリクエストを送信
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # モデルを指定
            messages=[
                {"role": "system", "content": "あなたは食材の保存方法に関する専門家です。"},
                {"role": "user", "content": text}
            ],
            max_tokens=300,
            temperature=0.7,
        )
        
        # 応答テキストを取得
        response_text = response['choices'][0]['message']['content'].strip()
        print(f"AIの応答 = {response_text}")
        return response_text
    
    except Exception as e:
        # エラーが発生した場合の処理
        error_message = f"エラーが発生しました: {e}"
        print(error_message)
        return error_message

def food_management(request):
    user = request.user
    sort_order = request.GET.get('sort', 'select')  # Default is 'select'
    print(sort_order)
    if sort_order == 'select':
        inventory_log = Inventorylog.objects.filter(user=user, expiration_date__gte=now()).order_by('expiration_date')
    elif sort_order == 'delete':
        inventory_log = Inventorylog.objects.filter(user=user, expiration_date__lt=now()).delete()
        inventory_log = Inventorylog.objects.filter(user=user, expiration_date__gte=now()).order_by('expiration_date')
    else:
        inventory_log = Inventorylog.objects.filter(user=user).order_by('expiration_date')
    print(inventory_log)
    context = {"inventory_log": inventory_log}
    return render(request, "app/food_management.html", context)

#レシピの消去
def food_management_delete(request, post_id):
    try:
        # Get the inventory item with the provided post_id
        inventorylog = Inventorylog.objects.get(id=post_id)
        inventorylog.delete()  # Delete the item
        
        # Show success message
        messages.success(request, "消去しました。")
    except Inventorylog.DoesNotExist:
        messages.error(request, "指定されたレシピが見つかりません。")
    
    # Redirect back to the food management page
    return redirect("/food_management/")

def ingredient_search(request):
    user = request.user
    selected_date = request.GET.get('date')
    
    # 在庫ログから指定された日付のエントリを取得
    inventorylog = Inventorylog.objects.filter(user=user, expiration_date=selected_date)
    # 在庫ログの食材名をもとにIngredientを検索
    ingredient = Ingredient.objects.filter(material__in=[log.ingredient_name for log in inventorylog])
    
    # ログイン中ならばアレルギーを取得する
    if request.user.is_authenticated:  # ユーザーがログインしている場合
        if request.user.allergy == "なし":
            allergies = []
        else:
            allergies = request.user.allergy.split(',')
    else:  # 未ログインのユーザーの場合
        allergies = []

    # 食材ごとにレシピを分類
    recipes_by_ingredient = defaultdict(list)
    for ing in ingredient:
        # Ingredientから関連レシピを取得
        recipes = Recipe.objects.filter(id=ing.recipe.id).annotate(average_rating=Avg('comment__rating')).order_by('-vote')
        
        # 各レシピにアレルギーフラグを設定
        for recipe in recipes:
            recipe.allergy_flag = Ingredient.objects.filter(recipe=recipe, material__in=allergies).exists()
        
        recipes_by_ingredient[ing.material].extend(recipes)
    
    print("++++{}++++".format(recipes_by_ingredient))
    
    # コンテキストに分類済みデータを渡す
    context = { 
        "recipes_by_ingredient": recipes_by_ingredient.items(),
    }
    if not inventorylog.exists():
        return render(request, "app/ingredients_management.html", context)
    else:
        return render(request, "app/ingredient_search.html", context)