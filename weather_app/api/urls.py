from django.urls import path
from weather_app.api import views

urlpatterns = [
   
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('index/', views.index, name='index'),
]