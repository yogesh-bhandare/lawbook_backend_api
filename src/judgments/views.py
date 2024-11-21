from rest_framework import viewsets
from .models import Judgment
from .serializers import JudgmentSerializer

class JudgmentViewSet(viewsets.ModelViewSet):
    queryset = Judgment.objects.all()
    serializer_class = JudgmentSerializer

