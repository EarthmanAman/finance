from django.db import models
from django.contrib.auth.models import User
from inflow.models import Investment, Loan


class CashOut(models.Model):
	user 			= models.OneToOneField(User, on_delete=models.CASCADE)

	date			= models.DateTimeField(auto_now_add=True)
	all_total		= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	active_total	= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)


class Debt(models.Model):
	cash_out 		= models.ForeignKey(CashOut, on_delete=models.PROTECT)
	loan 			= models.OneToOneField(Loan, on_delete=models.CASCADE)

	date 			= models.DateTimeField(auto_now_add=True)
	amount 			= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

	from_savings	= models.BooleanField(default=False)

class Loss(models.Model):
	cash_out 	= models.ForeignKey(CashOut, on_delete=models.PROTECT)
	investment 	= models.ForeignKey(Investment, null=True, on_delete=models.SET_NULL)

	date		= models.DateTimeField(auto_now_add=True)
	amount		= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

class Expense(models.Model):
	cash_out 		= models.ForeignKey(CashOut, on_delete=models.PROTECT)
	name 			= models.CharField(max_length=100)
	amount 			= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

	date			= models.DateTimeField(auto_now_add=True)

	from_savings	= models.BooleanField(default=False)
