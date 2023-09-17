from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Savings
from user.models import CustomUser
from .serializers import SavingsSerializer
import math

@api_view(['GET'])
def totalSavings(request, user_id):

    # Get the user
    try:
        user = get_object_or_404(CustomUser, id=user_id)
    except Exception as e:
        print(e)
        return Response({"erro": str(e)})

    # Get the user's savings
    savings = Savings.objects.filter(savings_owner=user)

    # Calculate the total savings
    total_savings = 0
    savings_number = 0
    for savings_product in savings:
        total_savings += savings_product.amount_saved
        savings_number += 1

    # Return the total savings
    return Response({"total_savings": total_savings, "savings_number": savings_number})


@api_view(['GET'])
def savingsPercentage(request, user_id):
    # Get the user
    try:
        user = get_object_or_404(CustomUser, id=user_id)
    except Exception as e:
        print(e)
        return Response({"erro": str(e)})

    # Get the user's savings
    savings = Savings.objects.filter(savings_owner=user)

    

    for data in savings:
        product_name = data.savings_name
        savings_goal = data.savings_goal
        amount_saved = data.amount_saved
        percentage = amount_saved / savings_goal * 100

        response = {"product_name": product_name, "percentage": math.floor(percentage)}
        print("stage")
        print()

        return Response(response)

