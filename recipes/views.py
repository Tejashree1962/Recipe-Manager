from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Favorite
from .forms import RecipeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# List all recipes
def recipe_list(request):
    recipes = Recipe.objects.all()
    favorites = Favorite.objects.values_list("recipe_id", flat=True)
    return render(
        request,
        "recipes/recipe_list.html",
        {"recipes": recipes, "favorites": favorites},
    )

# Recipe detail
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    is_favorite = Favorite.objects.filter(recipe=recipe).exists()
    return render(
        request,
        "recipes/recipe_detail.html",
        {"recipe": recipe, "is_favorite": is_favorite},
    )

# Create new recipe
@login_required
def recipe_create(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("recipe_list")
    else:
        form = RecipeForm()
    return render(request, "recipes/recipe_form.html", {"form": form})

# Update recipe
@login_required
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

# Delete recipe
@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.delete()
    return redirect("recipe_list")

# Toggle favorite (add/remove)
@login_required
def toggle_favorite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    fav, created = Favorite.objects.get_or_create(recipe=recipe)
    if not created:
        fav.delete()
    return redirect("recipe_list")

# List all favorite recipes
@login_required
def favorite_list(request):
    favorites = Favorite.objects.select_related("recipe")
    recipes = [fav.recipe for fav in favorites]
    return render(
        request,
        "recipes/favorite_list.html",
        {"recipes": recipes},
    )

# ✅ User Registration
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after register
            return redirect("recipe_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})
