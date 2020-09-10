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

	source 			= models.CharField(max_length=100, blank=True, null=True)
	date 			= models.DateTimeField(auto_now_add=True)
	amount 			= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	to 				= models.DateTimeField(auto_now_add=True, blank=True, null=True)

	is_active		= models.BooleanField(default=True)

class LoanPayment(models.Model):
	debt 	= models.ForeignKey(Debt, on_delete=models.CASCADE)
	loan 	= models.ForeignKey(Loan, on_delete=models.CASCADE, blank=True, null=True)
	amount 	= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	date 	= models.DateTimeField(auto_now_add=True)

	from_savings	= models.BooleanField(default=False)

class Loss(models.Model):
	cash_out 	= models.ForeignKey(CashOut, on_delete=models.PROTECT)
	investment 	= models.ForeignKey(Investment, null=True, on_delete=models.SET_NULL)

	date		= models.DateTimeField(auto_now_add=True)
	amount		= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	is_active		= models.BooleanField(default=True)

class Expense(models.Model):
	cash_out 		= models.ForeignKey(CashOut, on_delete=models.PROTECT)
	source 			= models.CharField(max_length=100)

	date			= models.DateTimeField(auto_now_add=True)
	is_active		= models.BooleanField(default=True)

class ExpenseIn(models.Model):
	expense 		= models.ForeignKey(Expense, on_delete=models.CASCADE, blank=True, null=True)
	date			= models.DateTimeField(auto_now_add=True)
	amount			= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	is_active		= models.BooleanField(default=True)

	from_savings	= models.BooleanField(default=False)