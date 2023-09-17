from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import CustomUser
from .models import TokenBlackList
from user.serializers import UserSerializer
from .serializers import TokenBlackListedSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.forms.models import model_to_dict
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import jwt


class Login(APIView):
    def post(self, request):
        # get post data
        request_data = request.data

        # checking email validity
        try:
            user = CustomUser.objects.get(email=request_data["email"])
            print("user found")
        except Exception as e:
            print(e)
            return Response({"error": "Please enter a valid email"})

        # checking password validity
        if user.check_password(request_data["password"]):
           
            # generating access and refres token
            refresh = RefreshToken.for_user(user)
            token = {
                "refresh_token": str(refresh),
                "access_token": str(refresh.access_token)
            }

            # serializing user data
            user_data = UserSerializer(user).data
            user_data["token"] = token

            return Response({"message": "User loged in successfully", "data": user_data})
        else:
             return Response({"error": "invalid password"})



class Logout(APIView):
    def post(self, request):
        # geting post data
        request_data = request.data

        # saving tokens to blackListed table
        serializer = TokenBlackListedSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()

        return Response({"message": "user Deleted successfully!!!!!!"})


class ForgetPassword(APIView):
    def post(self, request):
        # getting post data
        request_data = request.data
        current_site = "http://localhost:4200/forget-password-verificaton/"

        # checking if email is in database
        try:
            user = CustomUser.objects.get(email=request_data["email"])
        except Exception as e:
            print(e) 
            return Response({"error": "User does not exist!!!"})

        if user:
           # Generate verification token
            token = RefreshToken.for_user(user).access_token
            print("token generated")

            # generate verification link 
            current_site = current_site
            verification_url = f'{current_site}{token}'
            print("verification url generated")



            # This code is sending email and allowing me to pass a html content
            subject, from_email, to = "Password Recovery", "settings.EMAIL_HOST_USER", request_data["email"]
            text_content = "Click on the link below to reset your password"
            html_content = f"<p>Click on the link below to reset your password <br> <strong><a href={verification_url}> {verification_url} </a></strong>.</p>"
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            print("email sent")

            return Response({"message": "we have sent the password reset link to your email"}) 


class ResetPassword(APIView):
    def post(self, request, id):
        # get post data
        try:
            user = CustomUser.objects.get(pk=id)

            user.set_password(request.data["password"])
            user.save()

            return Response({"message": "password reset successfully"})
        except Exception as e:
            print(e)
            return Response({"message": "The links is no longer valid"})

            


class PasswordRecoveryVerify(APIView):
    def get(self, request, token):
        token_obj = ""

        try:
            # get token from link and decode to get id
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            print(decoded_token)
            id = decoded_token["user_id"]

            # using id to get user
            user = CustomUser.objects.get(pk=id)
            print("below is the user data:")
            print(user.first_name)

            print("Account Verified")

            serializer = UserSerializer(user)

            return Response({"message": "user verification successfull!!!!!", "redirectUrl": "http://localhost:4200/reset-password", "data": serializer.data})
        except Exception as e:
            print(str(e))
            user = None
            return Response({"message": "there was a problem decoding the token"})
       
        




