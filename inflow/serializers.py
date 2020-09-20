from itertools import chain

from django.db import models
from django.contrib.auth.models import User
from rest_framework.serializers import (
	HyperlinkedIdentityField,
	ModelSerializer, 
	SerializerMethodField,
	ListField,
	PrimaryKeyRelatedField,

	ValidationError,

	DateTimeField,
	DateField,
	IntegerField,
	ModelField,
	CharField,
	)

from outflow.models import Debt

from . models import (
		CashIn,
		Salary,
		Gift,
		Other,
		OtherIn,
		Investment,
		Profit,
		Loan,

		Saving,
	)

def all_total_cal(obj, is_active=None):

	if is_active == True:
		salaries = Salary.objects.filter(is_active=True)
		gifts = Gift.objects.filter(is_active=True)
		others = Other.objects.filter(is_active=True)
		investments = Investment.objects.filter(is_active=True)
		loans = Loan.objects.filter(is_active=True)
	elif is_active == False:
		salaries = Salary.objects.filter(is_active=False)
		gifts = Gift.objects.filter(is_active=False)
		others = Other.objects.filter(is_active=False)
		investments = Investment.objects.filter(is_active=False)
		loans = Loan.objects.filter(is_active=False)
	else:
		salaries = Salary.objects.all()
		gifts = Gift.objects.all()
		others = Other.objects.all()
		investments = Investment.objects.all()
		loans = Loan.objects.all()

	all_total = 0
	for salary in salaries:
		all_total += salary.amount

	for gift in gifts:
		all_total += gift.amount

	for other in others:
		for otherin in other.otherin_set.all():
			all_total += otherIn.amount
	for investment in investments:
		for profit in investment.profit_set.all():
			all_total += profit.amount

	for loan in loans:
		all_total += loan.amount

	return all_total

def savings_total(obj):
	savings = obj.saving_set.all()
	total = 0

	for saving in savings:
		total += saving.amount

	return total

class CashInSer(ModelSerializer):
	all_total = SerializerMethodField()
	active_total = SerializerMethodField()
	liquid_total = SerializerMethodField()
	savings = SerializerMethodField()
	months = SerializerMethodField()
	class Meta:
		model = CashIn
		fields = [
			"all_total",
			"active_total",
			"liquid_total",
			"savings",
			"months",
		]

	def get_all_total(self, obj):
		return all_total_cal(obj)

	def get_active_total(self, obj):
		return all_total_cal(obj, is_active=True)

	def get_liquid_total(self, obj):
		return all_total_cal(obj, is_active=True) - savings_total(obj)

	def get_savings(self, obj):
		return savings_total(obj)

	def get_months(self, obj):
		salaries = Salary.objects.filter(cash_in=obj)
		gifts = Gift.objects.filter(cash_in=obj)
		others_in = OtherIn.objects.filter(other__cash_in=obj)
		profits = Profit.objects.filter(investment__cash_in=obj)
		loans = Loan.objects.filter(cash_in=obj)

		totalQ = list(chain(salaries, gifts, others_in, profits, loans))
		months_dict = dict()
		for n in range(1, 13):

			total = sum([pay.amount for pay in totalQ if pay.date.month==n])
			active_total = sum([pay.amount for pay in totalQ if (pay.date.month==n and pay.is_active ==True)])
			
			savings = sum([pay.savings.amount for pay in totalQ if (pay.date.month==n and pay.is_active ==True and pay.savings)])
			
			months_dict[n] = { 
					"total": total,
					"active_total": active_total,
					"savings": savings,
					"salaries": {
						"total":sum([pay.amount for pay in salaries if (pay.date.month==n)]),
						"active_total":sum([pay.amount for pay in salaries if (pay.date.month==n and pay.is_active==True)]),
						"savings":sum([pay.savings.amount for pay in salaries if (pay.date.month==n and pay.is_active==True and pay.savings)]),
						},
					"gifts": {
						"total":sum([pay.amount for pay in gifts if (pay.date.month==n)]),
						"active_total":sum([pay.amount for pay in gifts if (pay.date.month==n and pay.is_active==True)]),
						"savings":sum([pay.savings.amount for pay in gifts if (pay.date.month==n and pay.is_active==True and pay.savings)]),
						},
					"others_in": {
						"total":sum([pay.amount for pay in others_in if (pay.date.month==n)]),
						"active_total":sum([pay.amount for pay in others_in if (pay.date.month==n and pay.is_active==True)]),
						"savings":sum([pay.savings.amount for pay in others_in if (pay.date.month==n and pay.is_active==True and pay.savings)]),
						},
					"profits": {
						"total":sum([pay.amount for pay in profits if (pay.date.month==n)]),
						"active_total":sum([pay.amount for pay in profits if (pay.date.month==n and pay.is_active==True)]),
						"savings":sum([pay.savings.amount for pay in profits if (pay.date.month==n and pay.is_active==True and pay.savings)]),
						},
					"loans": {
						"total":sum([pay.amount for pay in loans if (pay.date.month==n)]),
						"active_total":sum([pay.amount for pay in loans if (pay.date.month==n and pay.is_active==True)]),
						"savings":sum([pay.savings.amount for pay in loans if (pay.date.month==n and pay.is_active==True and pay.savings)]),
						},
					}
		return months_dict

class SalaryCreateSer(ModelSerializer):
	savings = IntegerField(
		required=False, 
		error_messages={
			"invalid": "Saving amount must be a number",
			})
	class Meta:
		model = Salary
		fields = [
			"cash_in",
			"source",
			"amount",
			"is_active",
			"savings",
		]

	def create(self, validated_data):
		is_active = validated_data.get("is_active")
		savings	  = validated_data.get("savings", 0)
		cash_in	  = validated_data.get("cash_in")
		amount = validated_data["amount"]
		savingIn = None

		if is_active and savings > 0:
			savingIn = Saving.objects.create(cash_in=cash_in, amount=savings)


		salary = Salary.objects.create(
			cash_in=cash_in, 
			source=validated_data["source"], 
			amount=validated_data["amount"], 
			is_active=is_active,
			savings=savingIn,
			)

		content = {
			"cash_in": cash_in,
			"source":validated_data["source"],
			"amount": amount,
			"is_active": is_active,
			"savings": savings,
		}
		return content

class SalaryListSer(ModelSerializer):
	savings = SerializerMethodField()
	class Meta:
		model = Salary
		fields = [
			"id",
			"cash_in",
			"source",
			"amount",
			"is_active",
			"savings",
			"date",
		]

	def get_savings(self, obj):
		if obj.savings:
			return obj.savings.amount
class SalaryDetailSer(ModelSerializer):
	savings = IntegerField(
		required=False, 
		error_messages={
			"invalid": "Saving amount must be a number",
			})
	class Meta:
		model = Salary
		fields = [
			"cash_in",
			"source",
			"amount",
			"date",
			"is_active",
			"savings",
		]

	def update(self, instance, validated_data):
		cash_in = validated_data.get("cash_in", instance.cash_in)
		amount = instance.amount
		savings = instance.savings

		savingIn = instance.savings
		if savingIn and validated_data.get("savings", instance.savings.amount) != savingIn.amount and validated_data.get("is_active", instance.is_active) == True:
			
			savingIn.amount = validated_data["savings"]
			savingIn.save()

		elif validated_data.get("savings", 0) > 0 and validated_data.get("is_active", None) == True:
			savingIn = Saving.objects.create(cash_in=cash_in, amount=validated_data["savings"])

		elif savings and validated_data.get("is_active", None) != instance.is_active and validated_data.get("is_active", None) == False:
			savingIn.amount = 0
			savingIn.save()
	
		instance.cash_in = validated_data.get("cash_in", instance.cash_in)
		instance.source  = validated_data.get("source", instance.source)
		instance.amount = validated_data.get("amount", instance.amount)
		instance.date = validated_data.get("date", instance.date)
		instance.is_active = validated_data.get("is_active", instance.is_active)
		instance.savings= savingIn
		instance.save()
		content = {
			"cash_in": instance.cash_in,
			"source":instance.source,
			"amount": instance.amount,
			"date": instance.date,
			"is_active": instance.is_active,
			"savings": instance.savings.amount,
		}
		return content

class GiftCreateSer(ModelSerializer):
	savings = IntegerField(
		required=True, 
		error_messages={
			"invalid": "Saving amount must be a number",
			})

	class Meta:
		model = Gift
		fields = [
			"cash_in",
			"source",
			"amount",
			"is_active",
			"savings",
		]

	def create(self, validated_data):
		is_active = validated_data.get("is_active")
		savings	  = validated_data.get("savings", 0)
		cash_in	  = validated_data.get("cash_in")
		amount = validated_data["amount"]
		savingIn = None

		if is_active and savings > 0:
			savingIn = Saving.objects.create(cash_in=cash_in, amount=savings)
			cash_in.active_total += amount


		gift = Gift.objects.create(
			cash_in=cash_in, 
			source=validated_data["source"], 
			amount=validated_data["amount"], 
			is_active=is_active,
			savings=savingIn,
			)

		cash_in.all_total += amount
		cash_in.save()
		content = {
			"cash_in": cash_in,
			"source":validated_data["source"],
			"amount": amount,
			"is_active": is_active,
			"savings": savings,
		}
		return content

class GiftListSer(ModelSerializer):
	savings = SerializerMethodField()
	class Meta:
		model = Gift
		fields = [
			"cash_in",
			"source",
			"amount",
			"is_active",
			"savings",
		]

	def get_savings(self, obj):
		if obj.savings:
			return obj.savings.amount
		

class GiftDetailSer(ModelSerializer):
	savings = IntegerField(
		required=False, 
		error_messages={
			"invalid": "Saving amount must be a number",
			})
	class Meta:
		model = Gift
		fields = [
			"cash_in",
			"source",
			"amount",
			"is_active",
			"savings",
		]

	def update(self, instance, validated_data):
		cash_in = validated_data.get("cash_in", instance.cash_in)
		amount = instance.amount
		savings = instance.savings

		savingIn = instance.savings
		if savingIn and validated_data.get("savings", instance.savings.amount) != savingIn.amount and validated_data.get("is_active", instance.is_active) == True:
			
			savingIn.amount = validated_data["savings"]
			savingIn.save()
		elif validated_data.get("savings", 0) > 0 and validated_data.get("is_active", None) == True:
			savingIn = Saving.objects.create(cash_in=cash_in, amount=validated_data["savings"])
		elif savings and validated_data.get("is_active", None) != instance.is_active and validated_data.get("is_active", None) == False:
			savingIn.amount = 0
			savingIn.save()

		instance.cash_in = validated_data.get("cash_in", instance.cash_in)
		instance.source  = validated_data.get("source", instance.source)
		instance.amount = validated_data.get("amount", instance.amount)
		instance.is_active = validated_data.get("is_active", instance.is_active)
		instance.savings= savingIn
		instance.save()
		content = {
			"cash_in": instance.cash_in,
			"source":instance.source,
			"amount": instance.amount,
			"is_active": instance.is_active,
			"savings": instance.savings.amount,
		}
		return content


class OtherCreateSer(ModelSerializer):
	
	class Meta:
		model = Other
		fields = [
			"cash_in",
			"source",
			"is_active",
		]

	

class OtherListSer(ModelSerializer):
	
	class Meta:
		model = Other
		fields = [
			"cash_in",
			"source",
			"is_active",
		]


class OtherInCreateSer(ModelSerializer):
	savings = IntegerField(
		required=False, 
		error_messages={
			"invalid": "Saving amount must be a number",
			})
	class Meta:
		model = OtherIn
		fields = [
			"other",
			"source",
			"amount",
			"is_active",
			"savings",
		]


	def create(self, validated_data):
		is_active = validated_data.get("is_active")
		savings	  = validated_data.get("savings", 0)
		other	  = validated_data.get("other")
		cash_in = other.cash_in

		amount = validated_data["amount"]

		savingIn = None

		if is_active and savings > 0:
			savingIn = Saving.objects.create(cash_in=cash_in, amount=savings)
			cash_in.active_total += amount


		otherIn = OtherIn.objects.create(
			other=other, 
			source= validated_data["source"],
			amount=validated_data["amount"], 
			is_active=is_active,
			savings=savingIn,
			)

		cash_in.all_total += amount
		cash_in.save()
		content = {
			"other": other,
			"amount": amount,
			"is_active": is_active,
			"savings": savings,
		}
		return content


class OtherInListSer(ModelSerializer):
	savings = SerializerMethodField()
	class Meta:
		model = OtherIn
		fields = [
			"other",
			"amount",
			"date",
			"is_active",
			"savings",
		]


	def get_savings(self, obj):
		if obj.savings:
			return obj.savings.amount


class OtherInDetailSer(ModelSerializer):
	savings = IntegerField(
		required=False, 
		error_messages={
			"invalid": "Saving amount must be a number",
			})
	class Meta:
		model = OtherIn
		fields = [
			"other",
			"amount",
			"date",
			"is_active",
			"savings",
		]


	def update(self, instance, validated_data):
		other = validated_data.get("other", instance.other)
		cash_in = other.cash_in
		amount = instance.amount
		savings = instance.savings

	

		savingIn = instance.savings
		if savingIn and validated_data.get("savings", instance.savings.amount) != savingIn.amount and validated_data.get("is_active", instance.is_active) == True:
			
			savingIn.amount = validated_data["savings"]
			savingIn.save()
		elif validated_data.get("savings", 0) > 0 and validated_data.get("is_active", None) == True:
			savingIn = Saving.objects.create(cash_in=cash_in, amount=validated_data["savings"])
		elif savings and validated_data.get("is_active", None) != instance.is_active and validated_data.get("is_active", None) == False:
			savingIn.amount = 0
			savingIn.save()
			
		instance.other = validated_data.get("other", instance.other)
		instance.amount = validated_data.get("amount", instance.amount)
		instance.date = validated_data.get("date", instance.date)
		instance.is_active = validated_data.get("is_active", instance.is_active)
		instance.savings= savingIn
		instance.save()
		content = {
			"other": instance.other,
			"amount": instance.amount,
			"date": instance.date,
			"is_active": instance.is_active,
			"savings": instance.savings.amount,
		}
		return content




class InvestmentCreateSer(ModelSerializer):
	
	class Meta:
		model = Investment
		fields = [
			"cash_in",
			"source",
			"date",
			"is_active",
		]

	

class InvestmentListSer(ModelSerializer):
	
	class Meta:
		model = Investment
		fields = [
			"cash_in",
			"source",
			"is_active",
		]




class ProfitCreateSer(ModelSerializer):
	savings = IntegerField(
		required=False, 
		error_messages={
			"invalid": "Saving amount must be a number",
			})
	class Meta:
		model = Profit
		fields = [
			"investment",
			"amount",
			"is_active",
			"savings",
		]


	def create(self, validated_data):
		is_active = validated_data.get("is_active")
		savings	  = validated_data.get("savings", 0)
		investment	  = validated_data.get("investment")
		cash_in = investment.cash_in

		amount = validated_data["amount"]

		savingIn = None

		if is_active and savings > 0:
			savingIn = Saving.objects.create(cash_in=cash_in, amount=savings)
			cash_in.active_total += amount


		profit = Profit.objects.create(
			investment=investment, 
			amount=validated_data["amount"], 
			is_active=is_active,
			savings=savingIn,
			)

		cash_in.all_total += amount
		cash_in.save()
		content = {
			"investment": investment,
			"amount": amount,
			"is_active": is_active,
			"savings": savings,
		}
		return content
	

class ProfitListSer(ModelSerializer):
	savings = SerializerMethodField()
	class Meta:
		model = Profit
		fields = [
			"investment",
			"amount",
			"date",
			"is_active",
			"savings",
		]


	def get_savings(self, obj):
		if obj.savings:
			return obj.savings.amount

class ProfitDetailSer(ModelSerializer):
	savings = IntegerField(
		required=False, 
		error_messages={
			"invalid": "Saving amount must be a number",
			})

	class Meta:
		model = Profit
		fields = [
			"investment",
			"amount",
			"date",
			"is_active",
			"savings",
		]


	def update(self, instance, validated_data):
		investment = validated_data["investment"]
		cash_in = investment.cash_in
		amount = instance.amount
		savings = instance.savings


		savingIn = instance.savings
		if savingIn and validated_data.get("savings", instance.savings.amount) != savingIn.amount and validated_data.get("is_active", instance.is_active) == True:
			
			savingIn.amount = validated_data["savings"]
			savingIn.save()
		elif validated_data.get("savings", 0) > 0 and validated_data.get("is_active", None) == True:
			savingIn = Saving.objects.create(cash_in=cash_in, amount=validated_data["savings"])
		elif savings and validated_data.get("is_active", None) != instance.is_active and validated_data.get("is_active", None) == False:
			savingIn.amount = 0
			savingIn.save()
			
		instance.investment = validated_data.get("investment", instance.investment)
		instance.amount = validated_data.get("amount", instance.amount)
		instance.is_active = validated_data.get("is_active", instance.is_active)
		instance.savings= savingIn
		instance.save()
		content = {
			"investment": instance.investment,
			"amount": instance.amount,
			"date": instance.date,
			"is_active": instance.is_active,
			"savings": instance.savings.amount,
		}
		return content



class LoanCreateSer(ModelSerializer):
	payback = IntegerField(
		required=True, 
		error_messages={
			"invalid": "Payback must be a number",
			})
	savings = IntegerField(
		required=False, 
		error_messages={
			"invalid": "Saving amount must be a number",
			})

	to = DateField(
		required=False, 
	)

	class Meta:
		model = Loan
		fields = [
			"cash_in",
			"source",
			"amount",
			"is_active",
			"savings",
			"payback",

			"to",
		]

	def create(self, validated_data):
		is_active = validated_data.get("is_active")
		savings	  = validated_data.get("savings", 0)
		cash_in	  = validated_data.get("cash_in")

		savingsIn = None
		if is_active and savings > 0:
			savingsIn = Saving.objects.create(cash_in=cash_in, amount=savings)
			
		cash_in.all_total += validated_data["amount"]
		cash_in.save()

		loan = Loan.objects.create(
			cash_in=cash_in,
			source= validated_data["source"], 
			amount=validated_data["amount"], 
			is_active=is_active,
			savings=savingsIn,
			)

		debt = Debt.objects.create(
			cash_out=cash_in.user.cashout, 
			loan = loan,
			amount=validated_data["payback"], 
			to= validated_data["to"]
			)
		content = {
			"cash_in": cash_in,
			"source": validated_data["source"],
			"amount": validated_data["amount"],
			"is_active": validated_data["is_active"],
			"svings": validated_data["savings"],
			"payback": validated_data["payback"],
			"to": validated_data["to"],
		}
		return content


	

class LoanListSer(ModelSerializer):
	
	savings = SerializerMethodField()
	payback = SerializerMethodField()
	to = SerializerMethodField()
	class Meta:
		model = Loan
		fields = [
			"id",
			"source",
			"amount",
			"is_active",
			"savings",

			"payback",
			"to",

		]

	def get_savings(self, obj):
		if obj.savings:
			return obj.savings.amount

	def get_payback(self, obj):
		try:
			return obj.debt.amount
		except:
			return None

	def get_to(self, obj):
		try:
			return obj.debt.to
		except:
			return None


class LoanDetailSer(ModelSerializer):
	
	payback = IntegerField(
		required=False, 
		error_messages={
			"invalid": "Payback must be a number",
			})
	savings = IntegerField(
		required=False, 
		error_messages={
			"invalid": "Saving amount must be a number",
			})

	to = DateField(
		required=False, 
	)

	class Meta:
		model = Loan
		fields = [
			"cash_in",
			"source",
			"amount",
			"is_active",
			"savings",

			"payback",
			"to",

		]

	def update(self, instance, validated_data):
		cash_in = validated_data.get("cash_in", instance.cash_in)
		amount = instance.amount
		savings = instance.savings

	

		savingIn = instance.savings
		if savingIn and validated_data.get("savings", instance.savings.amount) != savingIn.amount and validated_data.get("is_active", instance.is_active) == True:
			
			savingIn.amount = validated_data.get("savings", savings.amount)
			savingIn.save()
		elif validated_data.get("savings", 0) > 0 and validated_data.get("is_active", None) == True:
			savingIn = Saving.objects.create(cash_in=cash_in, amount=validated_data["savings"])
		elif savings and validated_data.get("is_active", None) != instance.is_active and validated_data.get("is_active", None) == False:
			savingIn.amount = 0
			savingIn.save()
			
		instance.cash = validated_data.get("cash", instance.cash_in)
		
		instance.amount = validated_data.get("amount", instance.amount)
		instance.is_active = validated_data.get("is_active", instance.is_active)
		instance.savings= savingIn
		instance.save()

		try:
			debt = instance.debt
		except:
			debt = None

		if debt:
			debt.payback = validated_data.get("payback", instance.payback)
			debt.to = validated_data.get("to", instance.to)
			debt.save()
		
		content = {
			"cash_in": instance.cash_in,
			"source": instance.source,
			"amount": instance.amount,
			"date": instance.date,
			"is_active": instance.is_active,
			"savings": instance.savings.amount,

			"payback": validated_data.get("payback",None),
			"to": validated_data.get("to",None)
		}

		return content

	
	
