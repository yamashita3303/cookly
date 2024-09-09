from django.contrib import admin
from .models import CustomUser, Recipe, Ingredient, Step

admin.site.register(CustomUser)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Step)