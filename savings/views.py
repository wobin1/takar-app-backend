from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Savings
from .serializers import SavingsSerializer
from alawi.helper import Payment
from wallet.models import Wallet
from user.models import CustomUser
from rest_framework import status
from takar.reused_functions import Functions

class SavingsProduct(APIView):
    
    # This code is creating an allowance product
    def post(self, request):
        # get post data
        request_data = request.data
        metadata = {
            "module": "savings"
        }
        
        # saving data to database
        serializer = SavingsSerializer(data=request_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            print("savings Product saved")
        
        # getting product data that was saved
        savingsData = serializer.data

        # getting user data  payment method from the helper file
        userData = Payment.getUser(request_data["savings_owner"])
        print(f"user data: {userData}")
        # generating payment data
        paymentData = {
            "amount": request_data["deposite"],
            "email": userData["userData"]["email"],
            "reference": savingsData["id"],
            "callback_url": "http://localhost:4200/app/savings",
            "metadata": metadata
        }
        print(paymentData)

        payment_handler = Payment.cardPayment(self, paymentData)


        # creating transaction history
        Functions.saveTransactionHistory(self, "Credit", request_data["deposite"], "savings product " + request_data["savings_name"] + "created", request_data["savings_owner"] )

        return Response({"message": "savings created successfully!!!", "data": [{"savigns_data":savingsData, "payment_data":payment_handler}]})


    def get(self, request):
            # getting all alowance products
            try:
                savings = Savings.objects.all()
            except Exception as e:
                print(e)

            # serializing allowance product
            if savings is not None:
                serializer = SavingsSerializer(savings, many=True)

            return Response({"data": serializer.data})

    def get(self, request, user_id):
        # checking if user is valid
        try:
            user = CustomUser.objects.get(id=user_id)
        except Exception as e:
            return Response({"error": str(e)})

        # getting user savings product
        if user is not None:
            user_savings = Savings.objects.filter(savings_owner=user_id).all()
            serializer = SavingsSerializer(user_savings, many=True) 

            for savings in serializer.data:
                amount_saved = savings["amount_saved"]
                savings_goal = savings["savings_goal"]
                percentage = amount_saved/savings_goal * 100

                print(percentage)

                savings["percentage"] = percentage

                print()


            return Response({"message": "success", "data": serializer.data})

class SavingsDetail(APIView):

        def get(self, request, savings_id):
            # checking if user is valid
            try:
                user = Savings.objects.get(id=savings_id)
            except Exception as e:
                return Response({"error": str(e)})

            # getting user savings product
            if user is not None:
                savings_detail = Savings.objects.filter(id=savings_id).all()
                serializer = SavingsSerializer(savings_detail, many=True) 

                return Response({"message": "success", "data": serializer.data})
