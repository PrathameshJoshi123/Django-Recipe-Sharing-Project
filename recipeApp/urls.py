"""
URL configuration for recipeApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from recipeApp import views
from Users import views as UserViews
from django.contrib.auth import views as auth_views
from Recipes import views as recipeViews
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', UserViews.register, name='register'),
    path('login1/', auth_views.LoginView.as_view(template_name='login.html', next_page='home'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('create-recipes/', recipeViews.create_recipe, name='create-recipe'),
    path('recipes/', recipeViews.recipe_list, name='recipeList'),
    path('recipe/<int:recipe_id>/', recipeViews.recipe_detail, name='recipeDetail'),
    path('my-recipes', recipeViews.my_recipes, name='myRecipes'),
    path('search/', recipeViews.search_recipes, name='searchRecipes'),
    path('save-recipe/<int:recipe_id>/', recipeViews.save_recipe, name='saveRecipe'),
    path('saved-recipe/', recipeViews.saved_recipes_view, name='savedRecipesView'),
    path('delete/<int:recipe_id>/', recipeViews.delete_recipe, name='delete_recipe'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
