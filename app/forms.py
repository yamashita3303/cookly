from django.forms import ModelForm
from .models import Recipe, Ingredient, Step

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