# recipes/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Favorite
from .forms import RecipeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# 🔑 MODIFIED: Only fetches recipes created by the current user.
@login_required 
def recipe_list(request):
    # Filter Recipe objects to only include those belonging to the logged-in user
    recipes = Recipe.objects.filter(user=request.user)
    
    # Filter Favorite objects to only include those belonging to the logged-in user
    favorites = Favorite.objects.filter(user=request.user).values_list("recipe_id", flat=True)
    
    return render(
        request,
        "recipes/recipe_list.html",
        {"recipes": recipes, "favorites": favorites},
    )

# 🔑 MODIFIED: Only checks if the CURRENT user has favorited this recipe.
@login_required 
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    
    # Check if the current user has favorited this specific recipe
    is_favorite = Favorite.objects.filter(recipe=recipe, user=request.user).exists()
    
    return render(
        request,
        "recipes/recipe_detail.html",
        {"recipe": recipe, "is_favorite": is_favorite},
    )

# 🔑 MODIFIED: Assigns the logged-in user to the new recipe upon creation.
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

# 🔑 MODIFIED: Links the favorite action to the specific user.
@login_required
def toggle_favorite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    
    # Get or create the Favorite instance linked to THIS recipe and THIS user
    fav, created = Favorite.objects.get_or_create(recipe=recipe, user=request.user)
    
    if not created:
        fav.delete()
    return redirect("recipe_list")

# 🔑 MODIFIED: Only lists favorite recipes for the current user.
@login_required
def favorite_list(request):
    # Filter favorites to only include those belonging to the logged-in user
    favorites = Favorite.objects.filter(user=request.user).select_related("recipe")
    recipes = [fav.recipe for fav in favorites]
    return render(
        request,
        "recipes/favorite_list.html",
        {"recipes": recipes},
    )

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