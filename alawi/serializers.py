from rest_framework import serializers
from user.serializers import UserSerializer 
from .models import Alawi


from rest_framework import serializers
from .models import Alawi


class AlawiSerializer(serializers.ModelSerializer):
    # product_owner = UserSerializer(read_only=True)
    # reciepient = UserSerializer(read_only=True)
    
    class Meta:
        model = Alawi
        fields = ['id', 
                'product_owner', 
                'product_name',
                'payment_sequence',
                'amount_to_be_paid',
                'payment_date',
                'reciepient',
                'product_balance',
                'initial_deposite']


    def create(self, validated_data):
        alawi = Alawi(
            product_owner=validated_data["product_owner"],
            product_name=validated_data["product_name"],
            payment_sequence=validated_data["payment_sequence"],
            reciepient=validated_data["reciepient"],
            amount_to_be_paid = validated_data["amount_to_be_paid"],
            payment_date = validated_data["payment_date"]
        )

        alawi.save()
        return alawi