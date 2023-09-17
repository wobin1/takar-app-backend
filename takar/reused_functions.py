from rest_framework.response import Response
from transaction_history.models import History
from transaction_history.serializers import TransactionSerializer
import datetime


class Functions():

    def saveTransactionHistory(self, transaction_type, amount, description, customer_id):
        data = {
            "transaction_type": transaction_type,
            "transaction_amount": amount,
            "transaction_description": description,
            "customer_id": customer_id
        }
        print(data)

        serializer = TransactionSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            print("serialized")
            print(serializer.data)

        return Response({"message": "transaction history saved successfully", "data":serializer.data})

    
    def format_date(date):
        format = '%Y-%m-%d'
        new_date = datetime.date.strftime(date, format)

        return new_date 
