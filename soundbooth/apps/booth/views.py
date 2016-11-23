from django.views.generic import DetailView, ListView, UpdateView, CreateView

from .models import Recording, Schedule
from .forms import RecordingForm, ScheduleForm


class RecordingListView(ListView):
    model = Recording


class RecordingCreateView(CreateView):
    model = Recording
    form_class = RecordingForm

class RecordingDetailView(DetailView):
    model = Recording
    slug_field = 'uid'


class RecordingUpdateView(UpdateView):
    model = Recording
    form_class = RecordingForm
    slug_field = 'uid'


class ScheduleListView(ListView):
    model = Schedule


class ScheduleCreateView(CreateView):
    model = Schedule
    form_class = ScheduleForm

class ScheduleDetailView(DetailView):
    model = Schedule
    slug_field = 'uid'


class ScheduleUpdateView(UpdateView):
    model = Schedule
    slug_field = 'uid'
    form_class = ScheduleForm
