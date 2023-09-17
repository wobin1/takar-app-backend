from django.shortcuts import render
from .serializers import UserSerializer
from .models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.forms.models import model_to_dict
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import jwt




class UserList(APIView):

    def get(self, request):
        # geting all data from the database
        try:
            user = CustomUser.objects.all()
            serializer = UserSerializer(user, many=True)
            print(serializer)
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e))


# this class create a user, generate a verification link and send to user email for
# for account verification.
class UserCreate(APIView):
    # create user function
    def post(self, request):    
        request_data = request.data
        print(request_data)

        # serializes request data and save new user
        # try:
        serializer = UserSerializer(data=request_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        print("user saved")
        # except Exception as e:
        #     print(f"printing exception {e}")
        #     return Response({"message": str(e)})


        user = CustomUser.objects.get(pk=serializer.data["id"])

        print("user querried")

        # Generate verification token
        token = RefreshToken.for_user(user).access_token
        print(token)

        # generate verification link 
        current_site = request_data['current_site']
        verification_url = f'{current_site}{token}'
        print("verification url generated")

        userData= UserSerializer(user).data

        userData["verification_token"] = token
        print(userData)

        userSerializer = UserSerializer(user, data=userData)
        print("verification token saved")

        # This code is sending email and allowing me to pass a html content
        subject, from_email, to = "Account Activation", "settings.EMAIL_HOST_USER", request_data["email"]
        text_content = "Click on the link below to verify your email"
        html_content = f"<p>Click on the link below to verify your email <br> <strong><a href={verification_url}> {verification_url} </a></strong>.</p>"
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        print("email sent")

        return Response({"status": True, "message":"A verification link has been sent to your email address if it exist", "data":serializer.data})


class ResendVerificationEmail(APIView):
    # create user function
    def post(self, request):    
        request_data = request.data
        print(request_data)


        user = CustomUser.objects.get(request_data["email"])

        print("user querried")

        # Generate verification token
        token = RefreshToken.for_user(user).access_token
        print("token generated")

        # generate verification link 
        current_site = request_data['current_site']
        verification_url = f'{current_site}{token}'
        print("verification url generated")



        # This code is sending email and allowing me to pass a html content
        subject, from_email, to = "Account Activation", "settings.EMAIL_HOST_USER", request_data["email"]
        text_content = "Click on the link below to verify your email"
        html_content = f"<p>Click on the link below to verify your email <br> <strong><a href={verification_url}> {verification_url} </a></strong>.</p>"
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        print("email sent")

        return Response(serializer.data)




class UserUpdate(APIView):
    def put(self, request, id):
        # getting post data
        request_data = request.data

        # checking if user is in database
        user = CustomUser.objects.get(pk=id)

        # saving post data to database
        serializer = UserSerializer(user, data=request_data)
        if serializer.is_valid():
            serializer.save()
        
        return Response({"message": "User updated!", "data": serializer.data})
        
        

class UserDelete(APIView):
    def delete(self, request, id):
        # checking if user is in database
        user = CustomUser.objects.get(pk=id)

        user.delete()

        return Response({"message": "user deleted!!"})


class UserVerify(APIView):
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
        except Exception as e:
            print(str(e))
            user = None
            return Response({"message": "there was a problem decoding the token"})

        if user is not None:
            # verify token
            try:
                if user.verification_token == token:
                    print("token is valid")
            except (TokenError, ValueError):
                token_obj = None
                print("Token error")

            if token_obj is not None:
                user_serializer = UserSerializer(user, many=True)
                data = {
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "email": user.email,
                            "password": user.password,
                            "current_site": "http://127.0.0.1:8000/api/users/verify/",
                            "is_verified": True
                        }


                serializer = UserSerializer(user, data=data)
                if serializer.is_valid():
                    serializer.save()
                print("user verified")
                return Response({"message": "user verification successfull!!!!!", "status": True, "redirect_url": "http://localhost:4200"})

            else:
                return Response({"message":"message Token Invalid token", "status": False})

            