from django.shortcuts import render, redirect, get_object_or_404
from .forms import RecipeForm, CommentForm
from .models import Recipe, SavedRecipe, Comment
from django.contrib.auth.decorators import login_required

def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user  
            recipe.save()  
            return redirect('recipeList')
    else:
        form = RecipeForm()
    return render(request, 'createRecipe.html', {'form': form})



def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipeList.html', {'recipes': recipes})


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    comments = Comment.objects.filter(recipe=recipe)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.recipe = recipe
            new_comment.save()
            return redirect('recipeDetail', recipe_id=recipe_id)
    else:
        comment_form = CommentForm()

    try:
        ing = recipe.ingredients.split(',')
        ins = recipe.instructions.split('\\')

        context = {
        'recipe': recipe,
        'ingredients_list': ing,
        'instructions_list': ins,
        'comments': comments,
        'comment_form': comment_form,
        }
    except:
        context = {
        'recipe': recipe,
        'ingredients_list': recipe.ingredients,
        'instructions_list': recipe.instructions,
        'comments': comments,
        'comment_form': comment_form,
        }
    return render(request, 'recipeDetail.html', context)


@login_required
def my_recipes(request):
    user_recipes = Recipe.objects.filter(created_by=request.user)

    context = {
        'user_recipes': user_recipes
    }
    return render(request, 'myRecipes.html', context)


def search_recipes(request):
    query = request.GET.get('q')
    if query:
        recipes = Recipe.objects.filter(title__icontains=query) | \
                  Recipe.objects.filter(cuisine__icontains=query) | \
                  Recipe.objects.filter(dietary_restrictions__icontains=query)
    else:
        recipes = Recipe.objects.all()

    context = {
        'recipes': recipes
    }
    return render(request, 'recipeList.html', context)


def save_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if not SavedRecipe.objects.filter(user=request.user, recipe=recipe).exists():
        SavedRecipe.objects.create(user=request.user, recipe=recipe)

    return redirect('recipeDetail', recipe_id=recipe_id)

@login_required
def saved_recipes_view(request):
    saved_recipes = SavedRecipe.objects.filter(user=request.user).select_related('recipe')

    context = {
        'saved_recipes': saved_recipes
    }
    return render(request, 'savedRecipes.html', context)


def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    
    if recipe.created_by != request.user:
        return HttpResponseForbidden("You do not have permission to delete this recipe.")

    if request.method == 'POST':
        recipe.delete()
        return redirect('myRecipes') 
    
    return redirect('myRecipes')