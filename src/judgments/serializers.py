from rest_framework import serializers
from .models import Judgment

class JudgmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Judgment
        fields = ['id', 'case_id', 'date_added', 'content']