# serializers.py
from rest_framework import serializers

class StreamUserSerializer(serializers.Serializer):
    userId = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    image = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)

    def validate_userId(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("User ID cannot be empty")
        return value

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Name cannot be empty")
        return value