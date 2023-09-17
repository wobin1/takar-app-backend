from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "verification_token",
            "dob",
            "is_active",
            "is_superuser",
            "is_verified",
            "is_suspended"
        ]

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.save()
        return user