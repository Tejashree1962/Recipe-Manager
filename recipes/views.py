from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Favorite
from .forms import RecipeForm

def recipe_list(request):
    recipes = Recipe.objects.all()
    favorites = Favorite.objects.values_list("recipe_id", flat=True)
    return render(request, "recipes/recipe_list.html", {"recipes": recipes, "favorites": favorites})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    is_favorite = Favorite.objects.filter(recipe=recipe).exists()
    return render(request, "recipes/recipe_detail.html", {"recipe": recipe, "is_favorite": is_favorite})

def recipe_create(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("recipe_list")
    else:
        form = RecipeForm()
    return render(request, "recipes/recipe_form.html", {"form": form})

def recipe_update(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect("recipe_list")
    else:
        form = RecipeForm(instance=recipe)
    return render(request, "recipes/recipe_form.html", {"form": form})

def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.delete()
    return redirect("recipe_list")

def toggle_favorite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    fav, created = Favorite.objects.get_or_create(recipe=recipe)
    if not created:
        fav.delete()  # unfavorite if already exists
    return redirect("recipe_list")
