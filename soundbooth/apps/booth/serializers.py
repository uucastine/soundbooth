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
            'finished',
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
            'name',
            'created',
            'last_updated',
            'crontab',
            'duration',
            'next_date',
            'active',
        )
        extra_kwargs = {
            'url': {'lookup_field': 'uid'}
        }

