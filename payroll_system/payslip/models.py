from django.db import models

class Payslip(models.Model):
    employee_name = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    issued_date = models.DateField()

    def __str__(self):
        return f"{self.employee_name} - {self.issued_date}"

