
from django.contrib import admin
from django.urls import path

from . views import (
	DebtCreate,
	DebtList,
	DebtDetail,
	LoanPayCreate,
	LoanPayList,
	LoanPayDetail,
	LossCreate,
	LossList,
	LossDetail,
	ExpenseCreate,
	ExpenseList,
	ExpenseDetail,
	ExpenseInCreate,
	ExpenseInList,
	ExpenseInDetail,
	)
app_name = "outflow"

urlpatterns = [
    path('debt/create', DebtCreate.as_view(), name="debt_create"),
    path('debts', DebtList.as_view(), name="debts"),
    path('debts/<int:pk>', DebtDetail.as_view(), name="debts_detail"),

    path('loan_pay/create', LoanPayCreate.as_view(), name="loan_pay_create"),
    path('loan_pays', LoanPayList.as_view(), name="loan_pays"),
    path('loan_pays/<int:pk>', LoanPayDetail.as_view(), name="loan_pays_detail"),

    path('loss/create', LossCreate.as_view(), name="loss_create"),
    path('losss', LossList.as_view(), name="losss"),
    path('losss/<int:pk>', LossDetail.as_view(), name="losss_detail"),

    path('expense/create', ExpenseCreate.as_view(), name="expense_create"),
    path('expenses', ExpenseList.as_view(), name="expenses"),
    path('expenses/<int:pk>', ExpenseDetail.as_view(), name="expenses_detail"),

    path('expense_in/create', ExpenseInCreate.as_view(), name="expense_in_create"),
    path('expenses_in', ExpenseInList.as_view(), name="expenses_in"),
    path('expenses_in/<int:pk>', ExpenseInDetail.as_view(), name="expenses_in_detail"),
    
]
