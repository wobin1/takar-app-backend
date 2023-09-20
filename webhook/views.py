from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import CustomUser
from alawi.models import Alawi
from alawi.serializers import AlawiSerializer
from savings.models import Savings
from savings.serializers import SavingsSerializer

# Create your views here.
class WebhookHandler(APIView):

    def post(self, request):
        print("webhook working...")
        request_data = request.data
        print(request_data)
        reference = request_data["data"]["reference"]
        module = request_data["data"]["metadata"]["module"]
        print(module)
        # user = CustomUser.objects.get(email=customer["email"])
        # print(user.id)

        if module == "alawi":
            print("checking if product exist...")
            product = Alawi.objects.get(pk=reference)
            print(product)
            print("product exis!")
            
            print("getting product data")
            product_data = AlawiSerializer(product).data
            product_data["initial_deposite"] = request_data["data"]["amount"]
            product_data["product_balance"] = request_data["data"]["amount"]
            print("below is the product data")
            print(product_data)
            print("product data gotten!")

            print("saving product Data")
            serializer = AlawiSerializer(product, data=product_data)
            if serializer.is_valid():
                serializer.save()

            print("below is saved data")
            print(serializer.data)

            print("product Data saved")

            return Response({"message": "Product data updated", "data": serializer.data})

        elif module == "savings":
            print("checking if savings data exist")
            savings = Savings.objects.get(pk=reference)
            print(savings)
            print("savngs product exist!")
            
            print("getting savings data")
            savings_data = SavingsSerializer(savings).data
            savings_data["savings_amount"] = request_data["data"]["amount"]
            savings_data["amount_saved"] = request_data["data"]["amount"]
            print(savings_data)

            print("savings data gotten!")

            print("saving savings data..")
            serializer = SavingsSerializer(savings, data=savings_data)
            if serializer.is_valid():
                serializer.save()

            print(serializer.data)

            print("savings data saved!")

            return Response({"message": "Product data updated", "data": serializer.data})