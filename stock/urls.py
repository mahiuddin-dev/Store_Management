from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    path('', views.ProductList.as_view(), name='product_list'),
    path('add/', views.ProductAddView.as_view(), name='product_add'),
    path('product/<pk>/', views.OneProduct.as_view(), name='product'),
    path('update/<pk>/', views.ProductUpdate.as_view(), name='update'),
    path('delete/<pk>/', views.ProductDelete.as_view(), name='delete'),
]
