import os
import requests
from user.models import CustomUser
from user.serializers import UserSerializer


class Payment():

    def getUser(id):
        print(id)
        try:
            user = CustomUser.objects.get(pk=id)
           
        except Exception as e:
            print(f"getting user exception:", {e})
            return {"error": "user is not found"}

        if user:
            serializer = UserSerializer(user)
            userData = serializer.data
            
            return {"userData": userData}
   

    def cardPayment(self, Requestpayload):

        createUrl = 'https://api.paystack.co/transaction/initialize'
        headers = {
            'Authorization': "Bearer sk_test_742c225a4a56b8d57d7d45fa57f0b2e77cabc0cc",
            'Content-Type': 'application/json'
        }

        print(headers)

        payload = Requestpayload

        # making api call
        response = requests.post(createUrl, json=payload, headers=headers)

        return response.json()