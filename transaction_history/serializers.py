from rest_framework import serializers
from .models import History
from user.serializers import UserSerializer


class TransactionSerializer(serializers.ModelSerializer):
    # customer_id = UserSerializer(read_only=True)
    class Meta:
        model = History
        fields = [
            'id',
            'transaction_date',
            'transaction_type',
            'transaction_amount',
            'transaction_description',
            'customer_id',
        ]

        def create(self, validated_data, **kwargs):
            history = History(
                transaction_type=validated_data["transaction_type"],
                transaction_amount = validated_data["transaction_amount"],
                transaction_description = validated_data["transaction_description"],
                customer_id= validated_data["customer_id"],
            )

            History.save()
            return history