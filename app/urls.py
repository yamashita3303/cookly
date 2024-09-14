from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'app'

urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.recipe, name="recipe"),
    path("search/", views.search_recipes, name="searchrecipes"),
    path("recipe/<int:post_id>", views.detail, name="detail"),
    path("recipe/create/", views.recipe_create, name="recipe_create"),
    path("comment/<int:recipe_id>", views.comments, name="comments"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)