from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.recipe, name="recipe"),
    path("search/", views.search_recipes, name="searchrecipes"),
    path("recipe/<int:post_id>", views.detail, name="detail"),
]