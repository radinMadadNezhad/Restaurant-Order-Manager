from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='dashboard/', permanent=False), name='home'),
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
] 