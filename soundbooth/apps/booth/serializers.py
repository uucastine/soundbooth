from .models import Recording

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


