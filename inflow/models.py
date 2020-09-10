from django.db import models

from django.contrib.auth.models import User

class CashIn(models.Model):
	user 			= models.OneToOneField(User, on_delete=models.CASCADE)
	
	date 			= models.DateTimeField(auto_now_add=True)
	all_total 		= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	active_total	= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	liquid_total	= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

class CommonFields(models.Model):
	cash_in 	= models.ForeignKey(CashIn, on_delete=models.PROTECT)
	source 		= models.CharField(max_length=100)
	date 		= models.DateTimeField(auto_now_add=True)

	amount 		= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	is_active	= models.BooleanField(default=True)
	savings 	= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)


class Salary(CommonFields):
	pass

class Gift(CommonFields):
	pass

class Other(models.Model):
	cash_in		= models.ForeignKey(CashIn, on_delete=models.PROTECT)

	source		= models.CharField(max_length=100)
	date 		= models.DateTimeField(auto_now_add=True)
	is_active	= models.BooleanField(default=True)

class OtherIn(models.Model):
	other 	= models.ForeignKey(Other, on_delete=models.PROTECT)

	amount		= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	date 		= models.DateTimeField(auto_now_add=True)

	is_active 	= models.BooleanField(default=True)
	savings 	= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

class Investment(models.Model):
	cash_in 	= models.ForeignKey(CashIn, on_delete=models.PROTECT)
	source 		= models.CharField(max_length=100)
	date 		= models.DateTimeField(auto_now_add=True)

	is_active	= models.BooleanField(default=True)

class Profit(models.Model):
	investment 	= models.ForeignKey(Investment, on_delete=models.PROTECT)

	amount		= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	date 		= models.DateTimeField(auto_now_add=True)

	is_active 	= models.BooleanField(default=True)
	savings 	= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

class Loan(CommonFields):
	pass


class Saving(models.Model):
	cash_in	= models.OneToOneField(CashIn, on_delete=models.PROTECT)
	amount 	= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)