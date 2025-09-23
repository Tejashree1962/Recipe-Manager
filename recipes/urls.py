from django.urls import path
from . import views

urlpatterns = [
    path("", views.recipe_list, name="recipe_list"),
    path("recipe/<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("recipe/new/", views.recipe_create, name="recipe_create"),
    path("recipe/<int:pk>/edit/", views.recipe_update, name="recipe_update"),
    path("recipe/<int:pk>/delete/", views.recipe_delete, name="recipe_delete"),
    path("recipe/<int:pk>/favorite/", views.toggle_favorite, name="toggle_favorite"),
]
