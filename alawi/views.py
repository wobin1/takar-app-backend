from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Alawi
from .serializers import AlawiSerializer
from .helper import Payment
from wallet.models import Wallet
from rest_framework import status
from takar.reused_functions import Functions
import schedule
import datetime



class Alowance(APIView):
    # This code is creating an allowance product
    def post(self, request):
        # get post data
        request_data = request.data
        metadata = {
            "module": "alawi"
        }
        # process payment
        print(request_data)
        
        # saving data to database
        serializer = AlawiSerializer(data=request_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            print("product saved")
        
        # getting product data that was saved
        productData = serializer.data

        # getting user data  payment method from the helper file
        userData = Payment.getUser(request_data["product_owner"])
        print(f"user data: {userData}")

        # generating payment data
        paymentData = {
            "amount": request_data["product_amount"],
            "email": userData["userData"]["email"],
            "reference": productData["id"],
            "callback_url": "http://localhost:4200/app/alawance",
            "metadata": metadata
        }

        payment_handler = Payment.cardPayment(self, paymentData)

        # creating transaction history
        Functions.saveTransactionHistory(self, "Credit", request_data["product_amount"], "Alawi product " + request_data["product_name"] + "created", request_data["product_owner"] )

        return Response({"message": "product created successfully!!!", "data": [{"product_data":productData, "payment_data":payment_handler}]})


    def get(self, request):
        # getting all alowance products
        try:
            allowance = Alawi.objects.all()
        except Exception as e:
            print(e)

        # serializing allowance product
        if allowance is not None:
            serializer = AlawiSerializer(allowance, many=True)

        

        return Response({"data": serializer.data})


    def get(self, request, product_id):
        # getting single alowance details
        allowance=""
        try:
            allowance = Alawi.objects.get(id=product_id)
        except Exception as e:
            print(e)

        # serializing allowance product
        if allowance is not None:
            serializer = AlawiSerializer(allowance)

        

        return Response({"data": serializer.data})


class User_Allowance(APIView):
    # This code is querying users allowance products
    def get(self, request, user_id):
        allowance=""
        # checking if user exist
        try:
            allowance = Alawi.objects.get(pk=user_id)
        except Exception as e:
            print(e)

        # serializing allowance product
        if allowance is not None:
            user_allowance = Alawi.objects.filter(product_owner=user_id).all()
            serializer = AlawiSerializer(user_allowance , many=True)

            return Response({"data": serializer.data})


class CardPayment(APIView):

    # This code is funding the created allowance product
    def post(self, request):
        request_data = request.data 

        payment_handler = Payment.cardPayment(self, request_data)

        return Response({"message": "Request successfull!!!", "data": payment_handler})



class FundWallet(APIView):

    # this code funds a wallet
    def fund_wallet(self, product_id):
        print("funding in progress...")
        request_data = {"product_id": product_id}
        print(request_data["product_id"])

        try:
            print("verification in progress")
            allowance = Alawi.objects.get(pk=request_data["product_id"])
            wallet = Wallet.objects.get(user=allowance.product_owner)
            serializer = AlawiSerializer(allowance)
            transaction_owner = serializer.data["reciepient"]
            print("verification done")
        except Exception as e:
            print("exception was printed")
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)


        if allowance is not None:
            print("crediting wallet in progress...")
            allowance.product_balance -= allowance.amount_to_be_paid
            wallet.balance += allowance.amount_to_be_paid

            allowance.save()
            wallet.save()
            print("wallet crediteded")

            # creating transaction history
            print("creating transaction history in progress")
            print(allowance.product_owner)
            Functions.saveTransactionHistory(self, "Product funding wallet", allowance.amount_to_be_paid, "wallet fund", transaction_owner )
            print("transaction history created")

        return {"message": f"{transaction_owner} has been funded with {allowance.amount_to_be_paid}"}


    # This code loops through all Alawi product to find 
    # to find schedule for payment that day
    def check_payment_for_today(self):
        allowance = Alawi.objects.all()
        data = []
        todays_date = Functions.format_date(datetime.date.today())

        for alawi in allowance:
            date = Functions.format_date(alawi.payment_date)

            if todays_date == date:
                data.append(alawi.id)
        
        return data

    # this code run through all allowance everyday and funds all funds accounts 
    # expecting money That day.
    def post(self, request):
        check = self.check_payment_for_today()
        payment_status = []

        for product in check:
            payment = self.fund_wallet(product)  
            payment_status.append(payment)           

        return Response({"message": "payment successfull", "detail": payment_status})
        
        

        

            



