from django.urls import path

from client import views

app_name = 'client'

urlpatterns = [
    path('', views.ClientList.as_view(), name='client_list'),
    path('add/', views.ClientAddView.as_view(), name='client_add'),
    path('profile/<pk>/', views.ClientProfile.as_view(), name='client_profile'),
    path('update/<pk>/', views.ClientProfileUpdate.as_view(), name='client_profile_update'),
    path('delete/<pk>/', views.ProfileDelete.as_view(), name='client_profile_delete'),
    path('get-names/', views.get_names, name='get_name'),
    path('profile/<pk>/checkout/', views.OrderCheckout.as_view(), name='checkout'),
    path('profile/<pk>/invoice/', views.InvoiceView.as_view(), name='invoice'),
    path('profile/<pk>/invoice/<int:int>/', views.invoice_detail, name='invoice_detail'),
    path('profile/<pk>/installments/', views.InstallmentsView.as_view(), name='installments'),
]
