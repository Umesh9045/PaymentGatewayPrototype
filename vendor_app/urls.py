from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.vender_manage, name='all_vendors'),
]