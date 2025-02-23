from django.shortcuts import render
from .models import Payslip

def payslip_list(request):
    payslips = Payslip.objects.all()
    return render(request, 'payslip_list.html', {'payslips': payslips})

