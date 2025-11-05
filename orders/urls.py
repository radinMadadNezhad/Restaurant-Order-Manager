from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('contact/', views.contact, name='contact'),
    path('contact/success/', TemplateView.as_view(template_name='contact_success.html'), name='contact_success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('order/<str:order_type>/<int:order_id>/', views.view_order_details, name='view_order_details'),
    path('order/ingredient/<int:order_id>/edit/<int:item_id>/', views.edit_ingredient_order_item, name='edit_ingredient_order_item'),
    path('order/ingredient/<int:order_id>/add/<str:station>/', views.add_ingredient_to_order, name='add_ingredient_to_order'),
    path('order/ingredient/<int:order_id>/process/', views.process_ingredient_order, name='process_ingredient_order'),
    path('ingredient-order/create/', views.create_ingredient_order, name='create_ingredient_order'),
    path('ingredient-order/<int:order_id>/edit/', views.edit_ingredient_order, name='edit_ingredient_order'),
    path('shopping-order/create/', views.create_shopping_order, name='create_shopping_order'),
    path('shopping-order/<int:order_id>/confirm/', views.confirm_shopping_order, name='confirm_shopping_order'),
    path('shopping-order/<int:order_id>/complete/', views.complete_shopping_order, name='complete_shopping_order'),
    # Management dashboard
    path('management/', views.management_home, name='management_home'),
    # Users CRUD
    path('management/users/', views.management_users, name='management_users'),
    path('management/users/create/', views.management_user_create, name='management_user_create'),
    path('management/users/<int:pk>/edit/', views.management_user_edit, name='management_user_edit'),
    path('management/users/<int:pk>/delete/', views.management_user_delete, name='management_user_delete'),
    # Stations CRUD
    path('management/stations/', views.management_stations, name='management_stations'),
    path('management/stations/create/', views.management_station_create, name='management_station_create'),
    path('management/stations/<int:pk>/edit/', views.management_station_edit, name='management_station_edit'),
    path('management/stations/<int:pk>/delete/', views.management_station_delete, name='management_station_delete'),
    # Ingredients CRUD
    path('management/ingredients/', views.management_ingredients, name='management_ingredients'),
    path('management/ingredients/create/', views.management_ingredient_create, name='management_ingredient_create'),
    path('management/ingredients/<int:pk>/edit/', views.management_ingredient_edit, name='management_ingredient_edit'),
    path('management/ingredients/<int:pk>/delete/', views.management_ingredient_delete, name='management_ingredient_delete'),
    # Station-Ingredient assignments
    path('management/station-ingredients/', views.management_station_ingredients, name='management_station_ingredients'),
] 
