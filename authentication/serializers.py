from rest_framework import serializers
from .models import TokenBlackList


class TokenBlackListedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenBlackList
        fields = [
            "id",
            "access_token",
            "refresh_token"
        ]

    def create(self, validated_data):
        token = TokenBlackList(
            access_token=validated_data["access_token"],
            refresh_token=validated_data["refresh_token"]
        )

        token.save()
        return token