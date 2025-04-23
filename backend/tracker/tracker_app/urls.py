from django.urls import path
from . import views
from .views import manage_items, manage_item, manage_records

urlpatterns = [
    path('create_user/', views.create_user, name='create_user'),
    path('create_item/', views.create_item, name='create_item'),
    path('create_record/', views.create_record, name='create_record'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('list_items/', views.list_items, name='list_items'),
    path('update_item/', views.update_item, name='update_item'),
    path('delete_item/', views.delete_item, name='delete_item'),
    path('list_records/', views.list_records, name='list_records'),
    path('update_record/', views.update_record, name='update_record'),
    path('delete_record/', views.delete_record, name='delete_record'),
    path('items/', manage_items, name='manage_items'),
    path('items/<str:item_id>/', manage_item, name='manage_item'),
    path('items/<str:item_id>/records/', manage_records, name='manage_records'),
]