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


class SalaryCreateSer(ModelSerializer):
	
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
		savings	  = validated_data.get("savings")
		cash_in	  = validated_data.get("cash_in")

		if is_active and savings > 0:
			try:
				savingsIn = Saving.objects.get(cash_in=cash_in)
				savingsIn.amount += savings
				savingsIn.save()
			except:
				savingsIn = Saving.objects.create(cash_in=cash_in, amount=savings)

		salary = Salary.objects.create(
			cash_in=cash_in, 
			source=validated_data["source"], 
			amount=validated_data["amount"], 
			is_active=is_active,
			savings=savings,
			)

		return salary

class SalaryListSer(ModelSerializer):
	
	class Meta:
		model = Salary
		fields = [
			"source",
			"amount",
			"is_active",
			"savings",
		]


class GiftCreateSer(ModelSerializer):
	
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
		savings	  = validated_data.get("savings")
		cash_in	  = validated_data.get("cash_in")

		if is_active and savings > 0:
			try:
				savingsIn = Saving.objects.get(cash_in=cash_in)
				savingsIn.amount += savings
				savingsIn.save()
			except:
				savingsIn = Saving.objects.create(cash_in=cash_in, amount=savings)

		salary = Gift.objects.create(
			cash_in=cash_in, 
			source=validated_data["source"], 
			amount=validated_data["amount"], 
			is_active=is_active,
			savings=savings,
			)

		return salary

class GiftListSer(ModelSerializer):
	
	class Meta:
		model = Gift
		fields = [
			"source",
			"amount",
			"is_active",
			"savings",
		]



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
			"source",
			"date",
			"is_active",
		]


class OtherInCreateSer(ModelSerializer):
	
	class Meta:
		model = OtherIn
		fields = [
			"other",
			"amount",
			"is_active",
			"savings",
		]


	def create(self, validated_data):
		is_active = validated_data.get("is_active")
		savings	  = validated_data.get("savings")
		other	  = validated_data.get("other")

		if is_active and savings > 0:
			try:
				savingsIn = Saving.objects.get(cash_in=other.cash_in)
				savingsIn.amount += savings
				savingsIn.save()
			except:
				savingsIn = Saving.objects.create(cash_in=other.cash_in, amount=savings)

		otherIn = OtherIn.objects.create(
			other=other, 
			amount=validated_data["amount"], 
			is_active=is_active,
			savings=savings,
			)

		return otherIn

	

class OtherInListSer(ModelSerializer):
	
	class Meta:
		model = OtherIn
		fields = [
			"amount",
			"date",
			"is_active",
			"savings",
		]


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
			"source",
			"date",
			"is_active",
		]



class ProfitCreateSer(ModelSerializer):
	
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
		savings	  = validated_data.get("savings")
		investment	  = validated_data.get("investment")

		if is_active and savings > 0:
			try:
				savingsIn = Saving.objects.get(cash_in=investment.cash_in)
				savingsIn.amount += savings
				savingsIn.save()
			except:
				savingsIn = Saving.objects.create(cash_in=investment.cash_in, amount=savings)

		profit = Profit.objects.create(
			investment=investment, 
			amount=validated_data["amount"], 
			is_active=is_active,
			savings=savings,
			)

		return profit

	

class ProfitListSer(ModelSerializer):
	
	class Meta:
		model = Profit
		fields = [
			"amount",
			"date",
			"is_active",
			"savings",
		]


class LoanCreateSer(ModelSerializer):
	payback = IntegerField(
		required=True, 
		error_messages={
			"invalid": "Payback must be a number",
			})
	to = DateTimeField(
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
		savings	  = validated_data.get("savings")
		cash_in	  = validated_data.get("cash_in")

		if is_active and savings > 0:
			try:
				savingsIn = Saving.objects.get(cash_in=cash_in)
				savingsIn.amount += savings
				savingsIn.save()
			except:
				savingsIn = Saving.objects.create(cash_in=cash_in, amount=savings)

		loan = Loan.objects.create(
			cash_in=cash_in,
			source= validated_data["source"], 
			amount=validated_data["amount"], 
			is_active=is_active,
			savings=savings,
			)

		debt = Debt.objects.create(
			cash_out=cash_in.user.cash_out, 
			source= validated_data["source"],
			amount=validated_data["payback"], 
			to= validated_data["to"]
			)

		return loan


	

class LoanListSer(ModelSerializer):
	
	class Meta:
		model = Loan
		fields = [
			"source",
			"amount",
			"is_active",
			"savings",

		]