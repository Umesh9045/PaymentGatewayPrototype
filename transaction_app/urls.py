from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.all_transactions, name='all_transactions'),
]