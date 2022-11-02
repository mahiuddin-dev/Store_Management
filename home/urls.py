from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('staff/', views.StaffView.as_view(), name='staff'),
    # path('staff/update/<pk>/', views.staff_update, name='staff_update')
    # path('staff/<pk>', views.StaffDelete, name='staff_delete')
]
