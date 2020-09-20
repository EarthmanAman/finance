from django.db import models
from django.contrib.auth.models import User
from rest_framework.serializers import (
	HyperlinkedIdentityField,
	ModelSerializer, 
	SerializerMethodField,
	ListField,
	PrimaryKeyRelatedField,

	ValidationError,

	DateField,
	IntegerField,
	ModelField,
	CharField,
	)

from . models import (
	CashOut,
	Debt,
	LoanPayment,
	Loss,
	Expense,
	ExpenseIn
	)

class DebtCreateSer(ModelSerializer):


	class Meta:
		model = Debt
		fields = [
			"cash_out",
			"source",
			"amount",
			"is_active",
			"to",
		]


class DebtListSer(ModelSerializer):

	class Meta:
		model = Debt
		fields = [
			"id",
			"source",
			"amount",
			"is_active",
			"to",
		]

class LoanPayCreateSer(ModelSerializer):


	class Meta:
		model = LoanPayment
		fields = [
			"debt",
			"amount",
			"date",
			"from_savings",
		]


class LoanPayListSer(ModelSerializer):

	debt = SerializerMethodField()
	amount_left = SerializerMethodField()
	class Meta:
		model = LoanPayment
		fields = [
			"debt",
			"amount",
			"amount_left",
			"date",
			"from_savings",
		]

	def get_debt(self, obj):
		if obj.debt.loan:
			return obj.debt.loan.source
		return obj.debt.source

	def get_amount_left(self, obj):
		return obj.debt.amount - obj.amount


class LossCreateSer(ModelSerializer):


	class Meta:
		model = Loss
		fields = [
			"cash_out",
			"investment",
			"source",
			"amount",
			"date",
			"is_active",
		]


class LossListSer(ModelSerializer):
	
	class Meta:
		model = Loss
		fields = [
			"investment",
			"source",
			"amount",
			"date",
			"is_active",
		]


class ExpenseCreateSer(ModelSerializer):


	class Meta:
		model = Expense
		fields = [
			"cash_out",
			"source",
			"date",
			"is_active",
		]

class ExpenseListSer(ModelSerializer):


	class Meta:
		model = Expense
		fields = [
			"cash_out",
			"source",
			"date",
			"is_active",
		]

class ExpenseInCreateSer(ModelSerializer):


	class Meta:
		model = ExpenseIn
		fields = [
			"expense",
			"source",
			"amount",
			"date",
			"is_active",
			"from_savings",
		]


class ExpenseInListSer(ModelSerializer):

	
	class Meta:
		model = ExpenseIn
		fields = [
			"expense",
			"source",
			"amount",
			"date",
			"is_active",
			"from_savings",
		]

	

