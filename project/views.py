from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm, RecipeForm
from .models import Recipe
from django.utils import timezone
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
User = get_user_model()

# Create your views here.
@login_required(login_url='userLoginPage')
def playRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    if recipe.recipe_user != request.user:
        return redirect('userDashBoard')
    recipe.last_used = timezone.now()
    recipe.frequency += 1
    recipe.save()
    print(recipe.frequency)
    context = {'recipe': recipe, 'loggedin': request.user.is_authenticated}
    return render(request, 'playRecipe.html', context)

@login_required(login_url='userLoginPage')
def deleteRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    if recipe.recipe_user != request.user:
        return redirect('userDashBoard')
    recipe.delete()
    print('recipe deleted')
    return redirect('userDashBoard')

@login_required(login_url='userLoginPage')
def editRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    if recipe.recipe_user != request.user:
        return redirect('userDashBoard')
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('userDashBoard')
        else:
            context = {'form': form, 'loggedin': request.user.is_authenticated}
            return render(request, 'editRecipe.html', context)
    else:
        form = RecipeForm(initial={'recipe_name': recipe.recipe_name, 'recipe_steps': recipe.recipe_steps}, instance=recipe)
        context = {'form': form, 'loggedin': request.user.is_authenticated}
        return render(request, 'editRecipe.html', context)


@login_required(login_url='userLoginPage')
def createRecipe(request):
    form = RecipeForm(request.POST or None)
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.frequency = 0
        recipe.recipe_user = request.user
        recipe.last_used = timezone.now()
        recipe.save()
        return redirect('userDashBoard')
    context = {'form': form, 'loggedin': request.user.is_authenticated}
    return render(request, 'createRecipe.html', context)

@login_required(login_url='userLoginPage')
def userDashBoard(request):
    qs = Recipe.objects.all()
    qs = qs.filter(recipe_user=request.user)
    context = {'queryset': qs, 'loggedin': request.user.is_authenticated}
    return render(request, 'userDashBoard.html', context)

def userLoginPage(request):
    if request.user.is_authenticated:
        return redirect('userDashBoard')
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username').lower()
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect(userDashBoard)
    context = {'form': form, 'loggedin': request.user.is_authenticated}
    return render(request, 'userLoginPage.html', context)

def userRegistrationPage(request):
    if request.user.is_authenticated:
        return redirect('userDashBoard')
    next = request.GET.get('next')
    form = UserRegistrationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('userDashBoard')
    context = {
        'form': form, 'loggedin': request.user.is_authenticated
    }
    return render(request, "userRegistrationPage.html", context)

@login_required(login_url='userLoginPage')
def userLogoutPage(request):
    logout(request)
    return redirect('userLoginPage')