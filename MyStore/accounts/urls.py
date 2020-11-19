from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/register', views.register, name='register'),
    path("Home/create_stuff", views.create_Stuff, name="create_stuff"),
    path("Home/Search_Cashier", views.Search_Cashier, name="Search_Cashier"),
    path("Home/Update_Cashier", views.Update_Cashier, name="Update_Cashier"),
    path("Home/logout", views.logout, name="logout"),

]
