from rest_framework import serializers
from .models import Savings
from user.serializers import UserSerializer


class SavingsSerializer(serializers.ModelSerializer):
    # savings_owner = UserSerializer(read_only=True)
    # reciepient = UserSerializer(read_only=True)
    class Meta:
        model = Savings
        fields = ['id', 
                'savings_owner', 
                'savings_name', 
                'creation_date',
                'deadline',
                'savings_goal',
                'amount_saved', 
                'reciepient',
                ]


    def percentage():
        percent = amount_saved/savings_goal *100

        return percent

    def create(self, validated_data):
        savings = Savings(
            savings_owner=validated_data["savings_owner"],
            savings_name=validated_data["savings_name"],
            savings_goal=validated_data["savings_goal"],
            reciepient=validated_data["reciepient"]
        )

        savings.save()
        return savings