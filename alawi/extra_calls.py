from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Alawi
from user.models import CustomUser

@api_view(['GET'])
def totalAlawi(request, user_id):
    # Get the user
    try:
        user = get_object_or_404(CustomUser, id=user_id)
    except Exception as e:
        print(e)
        return Response({"erro": str(e)})

    # Get the user's savings
    alawi = Alawi.objects.filter(product_owner=user)

    # Calculate the total savings
    total_alawi = 0
    product_number = 0
    for alawi_product in alawi:
        total_alawi += alawi_product.product_balance
        product_number += 1

    # Return the total savings
    return Response({"alawi_balance": total_alawi, "product_number": product_number})