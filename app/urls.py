from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path("home/", views.recipe, name="recipe"),
    path("search/", views.search_recipes, name="searchrecipes"),
    path("recipe/<int:post_id>", views.detail, name="detail"),
    path("recipe/create/", views.recipe_create, name="recipe_create"),
    path('recipe/edit/<int:post_id>/', views.recipe_edit, name='edit'),
    path('recipe/delete/<int:post_id>', views.recipe_delete, name='delete'),
    path("comment/<int:recipe_id>", views.comments, name="comments"),
    path('mypage/', views.mypage, name='mypage'),
    path('calendar/', views.recipe_calendar, name='recipe_calendar'),
    path('ingredients_management/', views.ingredients_management, name='ingredients_management'),
    path('food_management/', views.food_management, name='food_management'),
    path('food_management/delete/<int:post_id>/', views.food_management_delete, name='food_management_delete'),
    path('ingredient_search/', views.ingredient_search, name='ingredient_search'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)