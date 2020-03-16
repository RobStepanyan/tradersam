from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ajax/search/', views.ajax_search, name='ajax-search'),
    path('ajax/hist/', views.ajax_hist, name='ajax-hist'),
    path('asset/<str:cntry>/<str:type_>/<str:pk>/', views.asset_details, name='asset-details'),
    path('news/', views.news_details, name='news-details'),
    path('all/<str:cntry>/<str:type_>/', views.all_assets, name='all-assets'),
    path('400/', views.error400, name='error400'),
    path('403/', views.error403, name='error403'),
    path('404/', views.error404, name='error404'),
]