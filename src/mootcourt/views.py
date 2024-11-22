import uuid  
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from stream_chat import StreamChat
from rest_framework.permissions import AllowAny
from decouple import config

STREAM_API_KEY=config("STREAM_API_KEY", default=None)
STREAM_API_SECRET=config("STREAM_API_SECRET", default=None)
CHAT_CLIENT = StreamChat(api_key=STREAM_API_KEY, api_secret=STREAM_API_SECRET)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"message": "Email and password are required."}, status=HTTP_400_BAD_REQUEST)

        if len(password) < 6:
            return Response({"message": "Password must be at least 6 characters."}, status=HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"message": "User already exists."}, status=HTTP_400_BAD_REQUEST)

        try:
            unique_id = uuid.uuid4().hex[:10]  

            user = User.objects.create(
                username=email,
                email=email,
                password=make_password(password),
            )

            CHAT_CLIENT.upsert_user({
                "id": unique_id,  
                "email": email,
                "name": email,
            })

            token = CHAT_CLIENT.create_token(unique_id)  

            return Response(
                {"token": token, "user": {"id": unique_id, "email": user.email}},
                status=HTTP_201_CREATED,
            )

        except Exception as e:
            return Response({"message": "Error creating user.", "details": str(e)}, status=HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
            if not check_password(password, user.password):
                raise ValidationError("Invalid credentials.")
            
            token = CHAT_CLIENT.create_token(str(user.id))
            return Response({"token": token, "user": {"id": user.id, "email": user.email}}, status=HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"message": "Invalid credentials."}, status=HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"message": str(e)}, status=HTTP_400_BAD_REQUEST)
