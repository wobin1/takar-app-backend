from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import History
from .serializers import TransactionSerializer
from takar.reused_functions import Functions


class TransactionHistory(APIView):

    def post(self, request):
        request_data = request.data
        print(request_data)

        #creating the transaction using Functions method
        history = Functions.saveTransactionHistory(self, request_data["transaction_type"], request_data["transaction_amount"], request_data["transaction_description"], request_data["customer_id"])
        print(history)
        serializer= TransactionSerializer(data=request_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()


        return Response("Transaction history created")

    def get(self, request):
        transactions = History.objects.all()

        serializer = TransactionSerializer(transactions, many=True)


        return Response({"data": serializer.data})


class TransactionDetail(APIView):
    def get(self, request, transaction_id):
        transactions = History.objects.get(id=transaction_id)

        serializer = TransactionSerializer(transactions)


        return Response({"data": serializer.data})


class UserTransaction(APIView):
    def get(self, request, user_id):  # Modify the method signature to include 'request' as the first argument
        transactions = History.objects.filter(customer_id=user_id).all()
        serializer = TransactionSerializer(transactions, many=True)

        return Response({"data": serializer.data})



class orderTransaction(APIView):
    def get(self, request, user_id):  # Modify the method signature to include 'request' as the first argument

        try:
            transactions = History.objects.filter(customer_id=user_id).order_by('-transaction_date')[:5]
        except Exception as e:
            print(e)
            return Response(str(e))

        print(transactions)
        serializer = TransactionSerializer(transactions, many=True)

        return Response({"data": serializer.data})


class ChartData(APIView):

    def get(self, request, user_id):
        try:
            transactions = History.objects.filter(customer_id=user_id)
        except Exception as e:
            print(e)
            return Response(str(e))
        # return Response("There was a problem with your request")

        chart_data = []
        expenses = []
        income = []
        for data in transactions:
            if data.transaction_type == "debit":
                expense = expenses.append(data.transaction_amount)

            if data.transaction_type == "credit":
                income.append(data.transaction_amount)

        chart_data.append({"data": expenses, "label": "Expenses"})
        chart_data.append({"data": income, "label": "Income"})

        return Response({"data": chart_data})