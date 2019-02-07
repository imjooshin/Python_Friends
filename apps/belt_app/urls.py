from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('friend/<int:user_id>', views.friend),
    path('unfriend/<int:user_id>', views.unfriend),
    path('user/<int:user_id>', views.user)
]