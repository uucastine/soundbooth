from django import forms

from .models import Recording, Schedule


class RecordingForm(forms.ModelForm):
    class Meta:
        model = Recording
        fields = ['audio_file', 's3_path']


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['date', 'rule']

