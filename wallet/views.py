from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Wallet
from .serializers import WalletSerializer
from rest_framework import status
from takar.reused_functions import Functions


class Wallets(APIView):

    def get(self, request):
        try:
            wallets= Wallet.objects.all()
        except Exception as e:
            print("wallet exception printed")
            return Response({"error": str(e)})


        if wallets is not None:
            serializer = WalletSerializer(wallets, many=True)
            return Response({"data": serializer.data})


class GetUserWallet(APIView):

    def get(self, request, user_id):
        try:
            user_wallet = Wallet.objects.get(user=user_id)
        except Exception as e:
            return Response({"error": str(e)})

        if user_wallet is not None:
            serializer = WalletSerializer(user_wallet)

            return Response({"message": "success", "data": serializer.data})

    


class TransferView(APIView):
    def post(self, request):
        sender_id = request.data.get('sender_id')
        recipient_id = request.data.get('recipient_id')
        amount = request.data.get('amount')

        try:
            sender_wallet = Wallet.objects.get(id=sender_id)
            recipient_wallet = Wallet.objects.get(id=recipient_id)
        except Wallet.DoesNotExist:
            return Response({'error': 'One or both wallets do not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if sender_wallet.balance < amount:
            return Response({'error': 'Insufficient funds.'}, status=status.HTTP_400_BAD_REQUEST)

        sender_wallet.balance -= amount
        recipient_wallet.balance += amount

        # creating credit transaction history
        Functions.saveTransactionHistory(self, "credit", amount, "", recipient_id )

        # creating debit transaction history
        Functions.saveTransactionHistory(self, "debit", amount, "", sender_id )

        sender_wallet.save()
        recipient_wallet.save()

        # saving debit history
        functions.saveTransactionHistory(debit, amount, "", sender_id)

        # saving credit history
        functions.saveTransactionHistory(credit, amount, "", reciever_id)

        return Response({'message': 'Transfer successful.'}, status=status.HTTP_200_OK)
