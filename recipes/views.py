from django.shortcuts import render, redirect, get_object_or_404
# ❌ MODIFIED: Removed Favorite from imports
from .models import Recipe 
from .forms import RecipeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# ❌ MODIFIED: Removed all favorites logic
@login_required 
def recipe_list(request):
    # Filter Recipe objects to only include those belonging to the logged-in user
    recipes = Recipe.objects.filter(user=request.user)
    
    # ❌ REMOVED: Filter Favorite objects logic
    # favorites = Favorite.objects.filter(user=request.user).values_list("recipe_id", flat=True)
    
    return render(
        request,
        "recipes/recipe_list.html",
        {"recipes": recipes}, # ❌ MODIFIED: Removed "favorites" from context
    )

# ❌ MODIFIED: Removed all favorites logic
@login_required 
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    
    # ❌ REMOVED: Favorite check logic
    # is_favorite = Favorite.objects.filter(recipe=recipe, user=request.user).exists()
    
    # ✅ FIX: Split ingredients into a list so template can loop without `splitlines` filter
    ingredients = recipe.ingredients.splitlines()

    return render(
        request,
        "recipes/recipe_detail.html",
        {
            "recipe": recipe,
            # ❌ REMOVED: "is_favorite" from context
            "ingredients": ingredients, 
        },
    )

@login_required
def recipe_create(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            # Save the form but don't commit to the database yet
            recipe = form.save(commit=False)
            # Assign the current user to the recipe
            recipe.user = request.user 
            # Now save the recipe
            recipe.save()
            return redirect("recipe_list")
    else:
        form = RecipeForm()
    return render(request, "recipes/recipe_form.html", {"form": form})

# Update recipe (Good practice to check if the current user owns the recipe)
@login_required
def recipe_update(request, pk):
    # Fetch recipe and ensure it belongs to the current user
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user) 
    
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect("recipe_list")
    else:
        form = RecipeForm(instance=recipe)
    return render(request, "recipes/recipe_form.html", {"form": form})

# Delete recipe (Good practice to check if the current user owns the recipe)
@login_required
def recipe_delete(request, pk):
    # Fetch recipe and ensure it belongs to the current user
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)
    recipe.delete()
    return redirect("recipe_list")

# ❌ REMOVED: toggle_favorite view function
# @login_required
# def toggle_favorite(request, pk):
#     recipe = get_object_or_404(Recipe, pk=pk)
#     fav, created = Favorite.objects.get_or_create(recipe=recipe, user=request.user)
#     if not created:
#         fav.delete()
#     return redirect("recipe_list")

# ❌ REMOVED: favorite_list view function
# @login_required
# def favorite_list(request):
#     favorites = Favorite.objects.filter(user=request.user).select_related("recipe")
#     recipes = [fav.recipe for fav in favorites]
#     return render(
#         request,
#         "recipes/favorite_list.html",
#         {"recipes": recipes},
#     )

# User Registration (No change needed here)
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("recipe_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})