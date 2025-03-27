from django.contrib import admin

import payment_methods_app
from payment_methods_app.models import Payment_Method

# Register your models here.
admin.site.register(Payment_Method)