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

from . serializers import (
	CashInSer,

	SalaryCreateSer,
	SalaryListSer,
	SalaryDetailSer,

	GiftCreateSer,
	GiftListSer,
	GiftDetailSer,

	OtherCreateSer,
	OtherListSer,

	OtherInCreateSer,
	OtherInListSer,
	OtherInDetailSer,

	InvestmentCreateSer,
	InvestmentListSer,

	ProfitCreateSer,
	ProfitListSer,
	ProfitDetailSer,

	LoanCreateSer,
	LoanListSer,
	LoanDetailSer,

	)

class CashInList(ListAPIView):
	serializer_class = CashInSer
	queryset = CashIn.objects.all()


class SalaryCreate(CreateAPIView):

	serializer_class = SalaryCreateSer
	queryset = Salary.objects.all()

class SalaryList(ListAPIView):
	serializer_class = SalaryListSer
	queryset = Salary.objects.all()

class SalaryDetail(RetrieveUpdateDestroyAPIView):
	queryset = Salary.objects.all()
	
	def get_serializer_class(self):
		method = self.request.method
		if method == "GET":
			return SalaryListSer
		elif method == "PUT":
			return SalaryDetailSer



class GiftCreate(CreateAPIView):

	serializer_class = GiftCreateSer
	queryset = Gift.objects.all()

class GiftList(ListAPIView):
	serializer_class = GiftListSer
	queryset = Gift.objects.all()

class GiftDetail(RetrieveUpdateDestroyAPIView):
	queryset = Gift.objects.all()
	
	def get_serializer_class(self):
		method = self.request.method
		if method == "GET":
			return GiftListSer
		elif method == "PUT":
			return GiftDetailSer

class OtherCreate(CreateAPIView):

	serializer_class = OtherCreateSer
	queryset = Other.objects.all()

class OtherList(ListAPIView):
	serializer_class = OtherListSer
	queryset = Other.objects.all()

class OtherDetail(RetrieveUpdateDestroyAPIView):
	serializer_class = OtherListSer
	queryset = Other.objects.all()
	

class OtherInCreate(CreateAPIView):
	serializer_class = OtherInCreateSer
	queryset = OtherIn.objects.all()

class OtherInList(ListAPIView):
	serializer_class = OtherInListSer
	queryset = OtherIn.objects.all()

class OtherInDetail(RetrieveUpdateDestroyAPIView):
	queryset = OtherIn.objects.all()

	def get_serializer_class(self):
		method = self.request.method
		if method == "GET":
			return OtherInListSer
		elif method == "PUT":
			return OtherInDetailSer
	
class InvestmentCreate(CreateAPIView):
	serializer_class = InvestmentCreateSer
	queryset = Investment.objects.all()

class InvestmentList(ListAPIView):
	serializer_class = InvestmentListSer
	queryset = Investment.objects.all()

class InvestmentDetail(RetrieveUpdateDestroyAPIView):
	serializer_class = InvestmentListSer
	queryset = Investment.objects.all()

	

class ProfitCreate(CreateAPIView):
	serializer_class = ProfitCreateSer
	queryset = Profit.objects.all()

class ProfitList(ListAPIView):
	serializer_class = ProfitListSer
	queryset = Profit.objects.all()

class ProfitDetail(RetrieveUpdateDestroyAPIView):
	queryset = Profit.objects.all()
	
	def get_serializer_class(self):
		method = self.request.method
		if method == "GET":
			return ProfitListSer
		elif method == "PUT":
			return ProfitDetailSer

class LoanCreate(CreateAPIView):
	serializer_class = LoanCreateSer
	queryset = Loan.objects.all()

class LoanList(ListAPIView):
	serializer_class = LoanListSer
	queryset = Loan.objects.all()

class LoanDetail(RetrieveUpdateDestroyAPIView):
	queryset = Loan.objects.all()

	def get_serializer_class(self):
		method = self.request.method
		if method == "GET":
			return LoanListSer
		elif method == "PUT":
			return LoanDetailSer
	