import unittest
from django.core.urlresolvers import reverse
from django.test import Client
from .models import Recording
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType


def create_django_contrib_auth_models_user(**kwargs):
    defaults = {}
    defaults["username"] = "username"
    defaults["email"] = "username@tempurl.com"
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_django_contrib_auth_models_group(**kwargs):
    defaults = {}
    defaults["name"] = "group"
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_django_contrib_contenttypes_models_contenttype(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_recording(**kwargs):
    defaults = {}
    defaults["uid"] = "uid"
    defaults["audio_file"] = "audio_file"
    defaults["in_progress"] = "in_progress"
    defaults["s3_path"] = "s3_path"
    defaults.update(**kwargs)
    return Recording.objects.create(**defaults)


class RecordingViewTest(unittest.TestCase):
    '''
    Tests for Recording
    '''
    def setUp(self):
        self.client = Client()

    def test_list_recording(self):
        url = reverse('booth_recording_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_recording(self):
        url = reverse('booth_recording_create')
        data = {
            "uid": "uid",
            "audio_file": "audio_file",
            "in_progress": "in_progress",
            "s3_path": "s3_path",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_recording(self):
        recording = create_recording()
        url = reverse('booth_recording_detail', args=[recording.id,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_recording(self):
        recording = create_recording()
        data = {
            "uid": "uid",
            "audio_file": "audio_file",
            "in_progress": "in_progress",
            "s3_path": "s3_path",
        }
        url = reverse('booth_recording_update', args=[recording.id,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


