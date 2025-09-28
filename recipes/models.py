# recipes/models.py

from django.db import models
from django.contrib.auth.models import User # 🔑 NEW IMPORT: For linking recipes to users

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    ingredients = models.TextField()
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 🔑 ADDED: Link the recipe to the user who created it.
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# Bookmark without users (just stores recipe ID in a table)
class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    # 🔑 ADDED: Link the favorite to the user who saved it.
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        # 🔑 ADDED: Ensures a user can only favorite a recipe once.
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"Favorite: {self.recipe.title} by {self.user.username}"