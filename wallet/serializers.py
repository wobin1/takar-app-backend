from rest_framework import serializers
from user.models import CustomUser
from .models import Wallet

class WalletSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance']
        read_only_fields = ['id']

    def create(self, validated_data):
        wallet = Wallet(
            user = validated_data["user"]
        )

        wallet.save()
        return wallet


