from django.contrib import admin

from . models import (
	CashOut,
	Debt,
	LoanPayment,
	Loss,
	Expense,
	ExpenseIn,
	)

admin.site.register(CashOut)
admin.site.register(Debt)
admin.site.register(LoanPayment)
admin.site.register(Loss)
admin.site.register(Expense)
admin.site.register(ExpenseIn)
