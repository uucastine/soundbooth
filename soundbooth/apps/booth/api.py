from rest_framework import viewsets, permissions

from .models import Recording, Schedule
from .serializers import (RecordingSerializer,
                          ScheduleSerializer)


class RecordingViewSet(viewsets.ModelViewSet):
    """ViewSet for the Recording class"""

    queryset = Recording.objects.all()
    serializer_class = RecordingSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'uid'




class ScheduleViewSet(viewsets.ModelViewSet):
    """ViewSet for the Schedule class"""

    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'uid'

    #def get_queryset(self):
    #    return Reservation.objects.filter(user=self.request.user)
