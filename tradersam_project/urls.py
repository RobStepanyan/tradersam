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
    path('', include('main_app.urls')), # base.html, chart.js, creative.js, table.js, home.js, asset_details, main/views:567, users_app/views:152
    # path('', main_views.csoon),
    
    path('signup/', users_views.signup, name='signup'),
    path('activate/<uidb64>/<token>/', users_views.signup_activation, name='signup-activate'),
    path('login/', users_views.login, name='login'),
    path('logout/', users_views.logout, name='logout'),
    path('account/', users_views.account, name='account'),
    path('account/password-reset/', users_views.password_reset, name='password-reset'),
    path('account/new-password/<uidb64>/<token>/', users_views.new_password, name='new-password'),
    path('ajax/account/', users_views.ajax_account, name='ajax-account'),
    path('ajax/account/change-username/', users_views.ajax_change_username, name='ajax-change-username'),
    path('ajax/account/change-email/', users_views.ajax_change_email, name='ajax-change-email'),
    path('account/change-email/<uidb64>/<token>/<new_email>', users_views.change_email, name='change-email'),#to receive the link sent to email
    path('ajax/account/change-password/', users_views.ajax_change_password, name='ajax-change-password'),
    path('ajax/account/watchlist/', users_views.ajax_watchlist, name='ajax-watchlist'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
