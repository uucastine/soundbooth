from .models import Recording, Schedule

from rest_framework import serializers


class RecordingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recording
        fields = (
            'id',
            'uid',
            'created',
            'last_updated',
            'audio_file',
            'in_progress',
            's3_path',
        )


class ScheduleSerializer(serializers.ModelSerializer):
    next_date = serializers.ReadOnlyField()

    class Meta:
        model = Schedule
        fields = (
            'id',
            'uid',
            'created',
            'last_updated',
            'time',
            'date',
            'rule',
            'next_date',
        )

