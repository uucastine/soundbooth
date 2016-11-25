from .models import Recording, Schedule

from rest_framework import serializers


class RecordingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recording
        lookup_field = 'uid'
        fields = (
            'id',
            'uid',
            'created',
            'last_updated',
            'audio_file',
            'in_progress',
            's3_path',
        )
        extra_kwargs = {
            'url': {'lookup_field': 'uid'}
        }


class ScheduleSerializer(serializers.ModelSerializer):
    next_date = serializers.ReadOnlyField()

    class Meta:
        model = Schedule
        lookup_field = 'uid'
        fields = (
            'id',
            'uid',
            'created',
            'last_updated',
            'time',
            'date',
            'rule',
            'next_date',
            'active',
        )
        extra_kwargs = {
            'url': {'lookup_field': 'uid'}
        }

