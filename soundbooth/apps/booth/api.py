from rest_framework import viewsets, permissions

from .models import Recording
from .serializers import RecordingSerializer


class RecordingViewSet(viewsets.ModelViewSet):
    """ViewSet for the Recording class"""

    queryset = Recording.objects.all()
    serializer_class = RecordingSerializer
    permission_classes = [permissions.IsAuthenticated]


