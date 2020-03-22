"""tradersam_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

import users_app.views as users_views
import main_app.views as main_views

urlpatterns = [
    path('donttouchtheadminpage/', admin.site.urls),
    path('dev/', include('main_app.urls')), # base.html, chart.js, creative.js, asset_details
    path('', main_views.csoon),
    
    path('signup/', users_views.signup, name='signup'),
    path('login/', users_views.login, name='login'),
    path('logout/', users_views.logout, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
