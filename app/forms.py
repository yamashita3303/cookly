from django import forms
from django.forms import ModelForm
from .models import Recipe, Ingredient, Step, Comment, Rating

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "recipe_title",
            "recipe_image",
            "detail_text",
            "genre",
        ]

class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = [
            "material",
            "amount",
        ]

class StepForm(ModelForm):
    class Meta:
        model = Step
        fields = [
            "step_number",
            "step_text",
            "step_image",
            "step_video",
        ]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            "comment",
            "review",
        ]
class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['rating'] # 評価
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, '★' * i) for i in range(1, 6)]),  # 1〜5の評価
        }