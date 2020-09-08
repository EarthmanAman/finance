from django.contrib import admin

from . models import (
	CashOut,
	Debt,
	Loss,
	Expense,
	)

admin.site.register(CashOut)
admin.site.register(Debt)
admin.site.register(Loss)
admin.site.register(Expense)
