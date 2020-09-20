from django.db import models
from django.contrib.auth.models import User
from inflow.models import Investment, Loan


class CashOut(models.Model):
	user 			= models.OneToOneField(User, on_delete=models.CASCADE)

	date			= models.DateField(auto_now=True)
	all_total		= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	active_total	= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)


	def __str__(self):
		return self.user.username + " :- Cash Out" 
		


class Debt(models.Model):
	cash_out 		= models.ForeignKey(CashOut, on_delete=models.PROTECT)
	loan 			= models.OneToOneField(Loan, on_delete=models.CASCADE, blank=True, null=True)

	source 			= models.CharField(max_length=100, blank=True, null=True)
	date 			= models.DateField(blank=True, null=True)
	amount 			= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	to 				= models.DateField(auto_now=True, blank=True, null=True)

	is_active		= models.BooleanField(default=True)

	def __str__(self):
		if self.source == None or self.source == "":
			return self.loan.source + " = payback = " + str(self.amount)
		return self.source + " = payback = " + str(self.amount)

class LoanPayment(models.Model):
	debt 			= models.ForeignKey(Debt, on_delete=models.CASCADE)
	amount 			= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	date 			= models.DateField(blank=True, null=True)

	from_savings	= models.BooleanField(default=False)

	def __str__(self):
		return self.debt.__str__() + " = payment = " + str(self.amount)

class Loss(models.Model):
	cash_out 		= models.ForeignKey(CashOut, on_delete=models.PROTECT)
	investment 		= models.ForeignKey(Investment, null=True, on_delete=models.SET_NULL)
	source 			= models.CharField(max_length=100, blank=True, null=True)
	date 			= models.DateField(blank=True, null=True)
	amount			= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	is_active		= models.BooleanField(default=True)

	def __str__(self):
		if self.investment:
			return self.investment.source
		return self.source

class Expense(models.Model):
	cash_out 		= models.ForeignKey(CashOut, on_delete=models.PROTECT)
	source 			= models.CharField(max_length=100)

	date 			= models.DateField(blank=True, null=True)
	is_active		= models.BooleanField(default=True)

	def __str__(self):
		return self.source

class ExpenseIn(models.Model):
	expense 		= models.ForeignKey(Expense, on_delete=models.CASCADE, blank=True, null=True)
	source 			= models.CharField(max_length=100, blank=True, null=True)
	date 			= models.DateField(blank=True, null=True)
	amount			= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	is_active		= models.BooleanField(default=True)

	from_savings	= models.BooleanField(default=False)

	def __str__(self):
		if self.expense:
			return self.expense.source
		return str(self.source) + f" = {self.amount}"