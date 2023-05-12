from django.contrib import admin
from django.urls import path
from notes.views import *

urlpatterns = [
    path('', login, name="login"),
    path('register/', register, name="register"),
    path('logout/', logout, name="logout"),
    path('dashboard/', dashboard, name="dashboard"),
    path('notes/<str:functionality>/', notes, name="notes"),
]