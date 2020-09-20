from django.shortcuts import render

from rest_framework.generics import (
	GenericAPIView,
	CreateAPIView,
	DestroyAPIView,
	ListAPIView,
	ListCreateAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	RetrieveUpdateDestroyAPIView,
	)

from . models import (
	CashOut,
	Debt,
	LoanPayment,
	Loss,
	Expense,
	ExpenseIn,
	)

from . serializers import (
	DebtCreateSer,
	DebtListSer,
	LoanPayCreateSer,
	LoanPayListSer,
	LossCreateSer,
	LossListSer,
	ExpenseCreateSer,
	ExpenseListSer,
	ExpenseInCreateSer,
	ExpenseInListSer,

	)


class DebtCreate(CreateAPIView):

	serializer_class = DebtCreateSer
	queryset = Debt.objects.all()

class DebtList(ListAPIView):

	serializer_class = DebtListSer
	queryset = Debt.objects.all()

class DebtDetail(RetrieveUpdateDestroyAPIView):

	serializer_class = DebtListSer
	queryset = Debt.objects.all()


class LoanPayCreate(CreateAPIView):

	serializer_class = LoanPayCreateSer
	queryset = LoanPayment.objects.all()

class LoanPayList(ListAPIView):

	serializer_class = LoanPayListSer
	queryset = LoanPayment.objects.all()

class LoanPayDetail(RetrieveUpdateDestroyAPIView):

	serializer_class = LoanPayListSer
	queryset = LoanPayment.objects.all()



class LossCreate(CreateAPIView):

	serializer_class = LossCreateSer
	queryset = Loss.objects.all()

class LossList(ListAPIView):

	serializer_class = LossListSer
	queryset = Loss.objects.all()

class LossDetail(RetrieveUpdateDestroyAPIView):

	serializer_class = LossListSer
	queryset = Loss.objects.all()



class ExpenseCreate(CreateAPIView):

	serializer_class = ExpenseCreateSer
	queryset = Expense.objects.all()

class ExpenseList(ListAPIView):

	serializer_class = ExpenseListSer
	queryset = Expense.objects.all()

class ExpenseDetail(RetrieveUpdateDestroyAPIView):

	serializer_class = ExpenseListSer
	queryset = Expense.objects.all()



class ExpenseInCreate(CreateAPIView):

	serializer_class = ExpenseInCreateSer
	queryset = ExpenseIn.objects.all()

class ExpenseInList(ListAPIView):

	serializer_class = ExpenseInListSer
	queryset = ExpenseIn.objects.all()

class ExpenseInDetail(RetrieveUpdateDestroyAPIView):

	serializer_class = ExpenseInListSer
	queryset = ExpenseIn.objects.all()