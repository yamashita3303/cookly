from django.contrib import admin
from .models import CustomUser, Recipe, Ingredient, Step, Comment, Allergy, Inventorylog

admin.site.register(CustomUser)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Step)
admin.site.register(Comment)
admin.site.register(Allergy)
admin.site.register(Inventorylog)