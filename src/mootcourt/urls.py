from django.urls import path
from .views import StreamTokenView

urlpatterns = [
    path('token/', StreamTokenView.as_view(), name='stream-token'),
]