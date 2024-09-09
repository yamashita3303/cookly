from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path("home", views.recipe, name="recipe"),
    path("search/", views.search_recipes, name="searchrecipes"),
    path("recipe/<int:post_id>", views.detail, name="detail"),
    path("recipe/create/", views.recipe_create, name="recipe_create"),
    path("recipe/<int:recipe_id>/detail/", views.detail_create, name="detail_create"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)