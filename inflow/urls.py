
from django.contrib import admin
from django.urls import path

from . views import (
		CashInList,

		SalaryCreate,
		SalaryList,
		SalaryDetail,

		GiftCreate,
		GiftList,
		GiftDetail,

		OtherCreate,
		OtherList,
		OtherDetail,

		OtherInCreate,
		OtherInList,
		OtherInDetail,

		InvestmentCreate,
		InvestmentList,
		InvestmentDetail,

		ProfitCreate,
		ProfitList,
		ProfitDetail,

		LoanCreate,
		LoanList,
		LoanDetail,
	)
app_name = "inflow"

urlpatterns = [
	path('cash_in', CashInList.as_view(), name="cash_in"),

    path('salary/create', SalaryCreate.as_view(), name="salary_create"),
    path('salarys', SalaryList.as_view(), name="salarys"),
    path('salarys/<int:pk>', SalaryDetail.as_view(), name="salarys_detail"),

    path('gift/create', GiftCreate.as_view(), name="gift_create"),
    path('gifts', GiftList.as_view(), name="gifts"),
    path('gifts/<int:pk>', GiftDetail.as_view(), name="gifts_detail"),

    path('other/create', OtherCreate.as_view(), name="other_create"),
    path('others', OtherList.as_view(), name="others"),
    path('others/<int:pk>', OtherDetail.as_view(), name="others_detail"),

    path('otherin/create', OtherInCreate.as_view(), name="otherin_create"),
    path('otherins', OtherInList.as_view(), name="otherins"),
    path('otherins/<int:pk>', OtherInDetail.as_view(), name="otherins_detail"),


    path('investment/create', InvestmentCreate.as_view(), name="investment_create"),
    path('investments', InvestmentList.as_view(), name="investments"),
    path('investments/<int:pk>', InvestmentDetail.as_view(), name="investments_detail"),

    path('profit/create', ProfitCreate.as_view(), name="profit_create"),
    path('profits', ProfitList.as_view(), name="profits"),
    path('profits/<int:pk>', ProfitDetail.as_view(), name="profits_detail"),

    path('loan/create', LoanCreate.as_view(), name="loan_create"),
    path('loans', LoanList.as_view(), name="loans"),
    path('loans/<int:pk>', LoanDetail.as_view(), name="loans_detail"),

]
