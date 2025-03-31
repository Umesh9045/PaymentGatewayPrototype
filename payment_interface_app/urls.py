from django.urls import path
from . import views

urlpatterns = [
    path('makepayment/<int:vendor_id>/<str:order_id>/<str:checkout_amount>/', views.make_payment, name='make_payment'),
    path('updatepayment/<int:transaction_id>/<int:payment_method_id>/<int:payment_status>/', views.payment_status_update, name='update_payment'),
]