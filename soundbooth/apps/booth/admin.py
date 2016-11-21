from django.contrib import admin
from django import forms
from .models import Recording

class RecordingAdminForm(forms.ModelForm):

    class Meta:
        model = Recording
        fields = '__all__'


class RecordingAdmin(admin.ModelAdmin):
    form = RecordingAdminForm
    list_display = ['uid', 'created', 'last_updated', 'audio_file', 'in_progress', 's3_path']
    readonly_fields = ['uid', 'created', 'last_updated', 'audio_file', 'in_progress', 's3_path']

admin.site.register(Recording, RecordingAdmin)


