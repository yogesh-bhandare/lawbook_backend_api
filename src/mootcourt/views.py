from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decouple import config
from getstream import Stream
from getstream.models import UserRequest
import logging
from .serializers import StreamUserSerializer

logger = logging.getLogger(__name__)

class StreamTokenView(APIView):
    def post(self, request):
        try:
            # Validate request data using serializer
            serializer = StreamUserSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get validated data
            validated_data = serializer.validated_data

            # Get Stream API credentials
            STREAM_API_KEY = config("STREAM_API_KEY", default=None)
            STREAM_API_SECRET = config("STREAM_API_SECRET", default=None)

            if not STREAM_API_KEY or not STREAM_API_SECRET:
                return Response(
                    {"error": "Stream API configuration is missing"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Initialize Stream client
            client = Stream(
                api_key=STREAM_API_KEY,
                api_secret=STREAM_API_SECRET,
                timeout=3.0
            )

            # Prepare custom data
            custom_data = {
                "email": validated_data.get('email'),
            }

            # Create or update user in Stream
            client.upsert_users(
                UserRequest(
                    id=validated_data['userId'],
                    name=validated_data['name'],
                    image=validated_data['image'],
                    role="user",
                    custom=custom_data
                ),
            )

            token = client.create_token(user_id=validated_data['userId'], expiration=3600)

            return Response({
                "token": token,
            })

        except Exception as e:
            logger.error(f"Error generating Stream token: {str(e)}")
            return Response(
                {"error": "Failed to generate token"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
