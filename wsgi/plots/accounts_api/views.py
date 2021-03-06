from accounts_api import serializers
from rest_framework import generics
from rest_framework.response import Response
from accounts_api.models import Sale, EMI, EMI_schedule, SaleTransaction, Expenses
from plots.lib.utils import EMI_CALCULATOR
from dateutil import rrule
from datetime import datetime, date
from django.http import Http404
from rest_framework import status


class CreateSales(generics.CreateAPIView):

    serializer_class = serializers.CreateSalesSerializer

    def perform_create(self, serializer):
        sale = serializer.save()
        self.create_transactions(sale)

    def create_transactions(self, sale):
        booking = sale.booking
        status = False
        if int(booking.booking_amount):
            if booking.booking_amount_method == "Cash":
                status = True
            booking_txn = SaleTransaction(sale=sale, amount=booking.booking_amount, source="Booking",
                                          trasaction_type=booking.booking_amount_method, trasaction_type_no=booking.booking_txn_no, status=status)
            booking_txn.save()
        status = False
        if int(booking.down_payment):
            if booking.down_payment_method == "Cash":
                status = True
            down_payment_txn = SaleTransaction(sale=sale, amount=booking.down_payment, source="Down Payment",
                                               trasaction_type=booking.down_payment_method, trasaction_type_no=booking.down_payment_txn_no, status=status)
            down_payment_txn.save()


class CreateEMI(generics.CreateAPIView):

    serializer_class = serializers.CreateEMISerializer

    def perform_create(self, serializer):
        emi = serializer.save()
        self.createEMI(emi)

    def createEMI(self, emi):
        monthly_emi = EMI_CALCULATOR(
            emi.total_amount, emi.intrest_rate, emi.duration).calc_emi()
        months = int(emi.duration)
        now = date(datetime.now().year, datetime.now().month, 7)
        tm = 0
        for dt in rrule.rrule(rrule.MONTHLY, dtstart=now):
            tm = tm + 1
            EMI_schedule(
                emi=emi, emi_schedule_date=dt, amount=monthly_emi).save()
            if tm == months:
                break


class ListSales(generics.ListAPIView):
    queryset = Sale.objects.filter(booking__booking_converted=True)
    serializer_class = serializers.ListSalesSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = serializers.ListSalesSerializer(queryset, many=True)
        return Response(serializer.data)


class ListEMI(generics.ListAPIView):
    queryset = EMI.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.ListEMISerializer(queryset, many=True)
        return Response(serializer.data)


class DetailsSales(generics.RetrieveAPIView):
    serializer_class = serializers.DetailsSalesSerializer

    def get_object(self, pk):
        try:
            return Sale.objects.get(pk=pk)
        except Sale.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        sales = self.get_object(pk)
        serializer = serializers.DetailsSalesSerializer(sales)
        return Response(serializer.data)


class DetailsEMI(generics.RetrieveAPIView):
    serializer_class = serializers.DetailsEMISerializer

    def get_object(self, pk):
        try:
            return EMI.objects.get(pk=pk)
        except EMI.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        emis = self.get_object(pk)
        serializer = serializers.DetailsEMISerializer(emis)
        return Response(serializer.data)


class DestroySales(generics.DestroyAPIView):
    serializer_class = serializers.SalesSerializer

    def get_object(self, pk):
        try:
            return Sale.objects.get(pk=pk)
        except Sale.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        sales = self.get_object(pk)
        sales.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DestroyEMI(generics.DestroyAPIView):
    serializer_class = serializers.EMISerializer

    def get_object(self, pk):
        try:
            return EMI.objects.get(pk=pk)
        except EMI.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        emi = self.get_object(pk)
        emi.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateSales(generics.UpdateAPIView):
    serializer_class = serializers.SalesUpdateSerializer

    def get_object(self, pk):
        try:
            return Sale.objects.get(pk=pk)
        except Sale.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        sale = self.get_object(pk)
        serializer = serializers.SalesUpdateSerializer(sale, data=request.data)
        if serializer.is_valid():
            sale = serializer.save()
            self.update_transactions(sale)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update_transactions(self, sale):
        SaleTransaction.objects.filter(sale=sale, status=False).delete()
        booking = sale.booking
        status = False
        if int(booking.booking_amount):
            if booking.booking_amount_method == "Cash":
                status = True
            booking_txn = SaleTransaction(sale=sale, amount=booking.booking_amount, source="Booking",
                                          trasaction_type=booking.booking_amount_method, trasaction_type_no=booking.booking_txn_no, status=status)
            booking_txn.save()
        status = False
        if int(booking.down_payment):
            if booking.down_payment_method == "Cash":
                status = True
            down_payment_txn = SaleTransaction(sale=sale, amount=booking.down_payment, source="Down Payment",
                                               trasaction_type=booking.down_payment_method, trasaction_type_no=booking.down_payment_txn_no, status=status)
            down_payment_txn.save()


class UpdateEMI(generics.UpdateAPIView):
    serializer_class = serializers.EMIUpdateSerializer

    def get_object(self, pk):
        try:
            return EMI.objects.get(pk=pk)
        except EMI.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        emi = self.get_object(pk)
        serializer = serializers.EMIUpdateSerializer(emi, data=request.data)
        if serializer.is_valid():
            emi = serializer.save()
            EMI_schedule.objects.filter(emi=emi, paid_status=False).delete()
            self.updateEMI(emi)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def updateEMI(self, emi):
        monthly_emi = EMI_CALCULATOR(
            emi.total_amount, emi.intrest_rate, emi.duration).calc_emi()
        months = int(emi.duration)
        now = date(datetime.now().year, datetime.now().month, 7)
        tm = 0
        for dt in rrule.rrule(rrule.MONTHLY, dtstart=now):
            tm = tm + 1
            EMI_schedule(
                emi=emi, emi_schedule_date=dt, amount=monthly_emi).save()
            if tm == months:
                break


class PayEMI(generics.UpdateAPIView):
    serializer_class = serializers.PayEMISerializer

    def get_object(self, pk):
        try:
            return EMI_schedule.objects.get(pk=pk)
        except EMI_schedule.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        emi = self.get_object(pk)
        serializer = serializers.PayEMISerializer(emi, data=request.data)
        if serializer.is_valid():
            emi = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTransactions(generics.CreateAPIView):

    serializer_class = serializers.CreateTransactionSerializer

    def perform_create(self, serializer):
        serializer.save()


class ListTransactions(generics.CreateAPIView):

    queryset = SaleTransaction.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.ListTransactionSerializer(queryset, many=True)
        return Response(serializer.data)


class UpdateTransactions(generics.UpdateAPIView):

    serializer_class = serializers.UpdateTransactionSerializer

    def get_object(self, pk):
        try:
            return SaleTransaction.objects.get(pk=pk)
        except SaleTransaction.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        sales_txn = self.get_object(pk)
        serializer = serializers.UpdateTransactionSerializer(
            sales_txn, data=request.data)
        if serializer.is_valid():
            sales_txn = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateTransactionStatus(generics.UpdateAPIView):

    serializer_class = serializers.UpdateTransactionStatusSerializer

    def get_object(self, pk):
        try:
            return SaleTransaction.objects.get(pk=pk)
        except SaleTransaction.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        sales_txn = self.get_object(pk)
        serializer = serializers.UpdateTransactionStatusSerializer(
            sales_txn, data=request.data)
        if serializer.is_valid():
            sales_txn = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DestroyTransactions(generics.DestroyAPIView):
    serializer_class = serializers.CreateTransactionSerializer

    def get_object(self, pk):
        try:
            return SaleTransaction.objects.get(pk=pk)
        except SaleTransaction.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        sales_txn = self.get_object(pk)
        sales_txn.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DetailsTransactions(generics.RetrieveAPIView):
    serializer_class = serializers.DetailsTransactionSerializer

    def get_object(self, pk):
        try:
            return SaleTransaction.objects.get(pk=pk)
        except SaleTransaction.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        sales_txn = self.get_object(pk)
        serializer = serializers.DetailsTransactionSerializer(sales_txn)
        return Response(serializer.data)


# Expenses views


class CreateExpenses(generics.CreateAPIView):

    serializer_class = serializers.CreateExpensesSerializer

    def perform_create(self, serializer):
        emi = serializer.save()


class ListExpenses(generics.ListAPIView):
    queryset = Expenses.objects.all()
    serializer_class = serializers.ListExpensesSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = serializers.ListExpensesSerializer(queryset, many=True)
        return Response(serializer.data)


class UpdateExpenses(generics.UpdateAPIView):

    serializer_class = serializers.UpdateExpensesSerializer

    def get_object(self, pk):
        try:
            return Expenses.objects.get(pk=pk)
        except Expenses.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        expenses = self.get_object(pk)
        serializer = serializers.UpdateExpensesSerializer(
            expenses, data=request.data)
        if serializer.is_valid():
            expenses = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DestroyExpenses(generics.DestroyAPIView):
    serializer_class = serializers.CreateExpensesSerializer

    def get_object(self, pk):
        try:
            return Expenses.objects.get(pk=pk)
        except Expenses.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        expenses = self.get_object(pk)
        expenses.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DetailsExpenses(generics.RetrieveAPIView):
    serializer_class = serializers.DetailsExpensesSerializer

    def get_object(self, pk):
        try:
            return Expenses.objects.get(pk=pk)
        except Expenses.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        expenses = self.get_object(pk)
        serializer = serializers.DetailsExpensesSerializer(expenses)
        return Response(serializer.data)
