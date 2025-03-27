from django.shortcuts import render
from .models import Vendor

# Create your views here.
def vender_manage(request):
     vendors = Vendor.objects.all()
     return render(request, 'manage.html', {'vendors': vendors})

