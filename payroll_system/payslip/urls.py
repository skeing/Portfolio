# -*- coding: utf-8 -*-
from django.urls import path
from .views import payslip_list

urlpatterns = [
    path('', payslip_list, name='payslip_list'),
]


