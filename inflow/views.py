from django.shortcuts import render

from . models import (
	CashIn,
	Salary,
	Gift,
	Other,
	Investment,
	Profit,
	Loan,
	Saving,
	)

from . serializers import (
	SalaryListSer,
	GiftCreateSer,
	GiftListSer,
	OtherCreateSer,
	OtherListSer,
	OtherInCreateSer,
	OtherInListSer,
	InvestmentCreateSer,
	InvestmentListSer,
	ProfitCreateSer,
	ProfitListSer,
	LoanCreateSer,
	LoanListSer,

	)
