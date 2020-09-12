"""bonHacketit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from project.views import userDashBoard, userLoginPage, userRegistrationPage, createRecipe, userLogoutPage, editRecipe, deleteRecipe, playRecipe, homePage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', userLoginPage, name="userLoginPage"),
    path('register/', userRegistrationPage, name="userRegistrationPage"),
    path('logout/', userLogoutPage, name="userLogoutPage"),
    path('dashboard/', userDashBoard, name="userDashBoard"),
    path('create/', createRecipe, name="createRecipe"),
    path('edit/<str:pk>', editRecipe, name="editRecipe"),
    path('delete/<str:pk>', deleteRecipe, name="deleteRecipe"),
    path('play/<str:pk>', playRecipe, name="playRecipe"),
    path('', homePage, name="homePage")
]
