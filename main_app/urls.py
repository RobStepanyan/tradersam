from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('error400/', views.error400, name='error400'),
    path('error403/', views.error403, name='error403'),
    path('error404/', views.error404, name='error404'),
]