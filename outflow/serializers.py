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
			"loan",
			"amount",
			"date",
			"from_savings",
		]

	def create(self, validated_data):
		from_savings = validated_data.get("from_savings")
		debt = validated_data.get("debt")

		if from_savings:
			saving = debt.cash_out.user.cash_in.saving
			saving.amount -= validated_data["amount"]
			saving.save()

		loan_pay = LoanPayment.objects.create(
				debt= validated_data["debt"],
				loan= validated_data["loan"],
				amount = validated_data["amount"],
				date= validated_data["date"],
				from_savings = validated_data["from_savings"]
			)

		return loan_pay

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
		return obj.debt.source

	def get_amount_left(self, obj):
		return obj.debt.amount - obj.amount



class LossCreateSer(ModelSerializer):


	class Meta:
		model = Loss
		fields = [
			"cash_out",
			"investment",
			"amount",
			"date",
			"is_active",
		]


class LossListSer(ModelSerializer):

	investment = SerializerMethodField()
	
	class Meta:
		model = Loss
		fields = [
			"investment",
			"amount",
			"date",
			"is_active",
		]


	def get_investment(self, obj):
		return obj.investment.source


class ExpenseCreateSer(ModelSerializer):


	class Meta:
		model = Expense
		fields = [
			"cash_out",
			"source",
			"date",
			"is_active",
		]


class LossListSer(ModelSerializer):

	
	class Meta:
		model = Expense
		fields = [
			"source",
			"date",
			"is_active",
		]




class ExpenseInCreateSer(ModelSerializer):


	class Meta:
		model = ExpenseIn
		fields = [
			"expense",
			"amount",
			"date",
			"is_active"
			"from_savings",
		]

	def create(self, validated_data):
		from_savings = validated_data.get("from_savings")
		expense = validated_data.get("expense")

		if from_savings:
			saving = expense.cash_out.user.cash_in.saving
			saving.amount -= validated_data["amount"]
			saving.save()

		expenseIn = ExpenseIn.objects.create(
				expense= validated_data["expense"],
				is_active= validated_data["is_active"],
				amount = validated_data["amount"],
				date= validated_data["date"],
				from_savings = validated_data["from_savings"]
			)

		return expenseIn

class ExpenseInListSer(ModelSerializer):

	expense = SerializerMethodField()
	
	class Meta:
		model = ExpenseIn
		fields = [
			"expense",
			"amount",
			"date",
			"is_active"
			"from_savings",
		]

	def get_expense(self, obj):
		return obj.expense.source

	

