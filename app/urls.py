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
    path('allergy/',views.allergy, name='allergy'),
    path("home/", views.recipe, name="recipe"),
    path("search/", views.search_recipes, name="searchrecipes"),
    path("recipe/<int:post_id>", views.detail, name="detail"),
    path("recipe/create/", views.recipe_create, name="recipe_create"),
    path('recipe/edit/<int:post_id>/', views.recipe_edit, name='edit'),
    path('recipe/delete/<int:post_id>', views.recipe_delete, name='delete'),
    path("comment/<int:recipe_id>", views.comments, name="comments"),
    path('mypage/', views.mypage, name='mypage'),
    path("favorite/<int:recipe_id>/", views.toggle_favorite, name="toggle_favorite"),
    path('follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
    path('author/<int:user_id>/', views.author_page, name='author_page'),
    path('recipe/<int:recipe_id>/comment/<int:comment_id>/reply/', views.reply_to_comment, name='reply_to_comment'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)