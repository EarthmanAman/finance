from django.contrib import admin

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

admin.site.register(CashIn)
admin.site.register(Salary)
admin.site.register(Gift)
admin.site.register(Other)
admin.site.register(OtherIn)
admin.site.register(Investment)
admin.site.register(Profit)
admin.site.register(Loan)
admin.site.register(Saving)

