from django.views.generic import DetailView, ListView, UpdateView, CreateView

from .models import Recording
from .forms import RecordingForm


class RecordingListView(ListView):
    model = Recording


class RecordingCreateView(CreateView):
    model = Recording
    form_class = RecordingForm

class RecordingDetailView(DetailView):
    model = Recording


class RecordingUpdateView(UpdateView):
    model = Recording
    form_class = RecordingForm

