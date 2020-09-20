from django.db import models

from django.contrib.auth.models import User

class CashIn(models.Model):
	user 			= models.OneToOneField(User, on_delete=models.CASCADE)
	
	date 			= models.DateField(auto_now=True)
	all_total 		= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	active_total	= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	liquid_total	= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

	def __str__(self):
		return self.user.username + " :- Cash In" 

class Saving(models.Model):
	cash_in	= models.ForeignKey(CashIn, on_delete=models.PROTECT)
	amount 	= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

	def __str__(self):
		return str(self.amount)


class CommonFields(models.Model):
	cash_in 	= models.ForeignKey(CashIn, on_delete=models.PROTECT)
	source 		= models.CharField(max_length=100)
	date 		= models.DateField(blank=True, null=True)

	amount 		= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	is_active	= models.BooleanField(default=True)
	savings 	= models.OneToOneField(Saving, on_delete=models.SET_NULL, blank=True, null=True)

	def __str__(self):
		return self.source

class Salary(CommonFields):
	pass

class Gift(CommonFields):
	pass

class Other(models.Model):
	cash_in		= models.ForeignKey(CashIn, on_delete=models.PROTECT)

	source		= models.CharField(max_length=100)
	date 		= models.DateField(auto_now=True)
	is_active	= models.BooleanField(default=True)

	def __str__(self):
		return self.source

class OtherIn(models.Model):
	other 		= models.ForeignKey(Other, on_delete=models.PROTECT)
	source 		= models.CharField(max_length=100, blank=True)
	amount		= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	date 		= models.DateField(blank=True, null=True)

	is_active 	= models.BooleanField(default=True)
	savings 	= models.OneToOneField(Saving, on_delete=models.SET_NULL, blank=True, null=True)

	def __str__(self):
		return self.other.source + " :- " + str(self.amount)

class Investment(models.Model):
	cash_in 	= models.ForeignKey(CashIn, on_delete=models.PROTECT)
	source 		= models.CharField(max_length=100)
	date 		= models.DateField(auto_now=True)

	is_active	= models.BooleanField(default=True)

	def __str__(self):
		return self.source

class Profit(models.Model):
	investment 	= models.ForeignKey(Investment, on_delete=models.PROTECT)

	amount		= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	date 		= models.DateField(blank=True, null=True)

	is_active 	= models.BooleanField(default=True)
	savings 	= models.OneToOneField(Saving, on_delete=models.SET_NULL, blank=True, null=True)

	def __str__(self):
		return self.investment.source + " :- " + str(self.amount)

class Loan(CommonFields):
	pass


