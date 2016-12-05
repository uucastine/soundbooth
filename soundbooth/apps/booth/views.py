from django.views.generic import DetailView, ListView, UpdateView, CreateView, TemplateView
from braces.views import AnonymousRequiredMixin
from django.core.urlresolvers import reverse_lazy


from .models import Recording, Schedule
from .forms import RecordingForm, ScheduleForm

class HomepageView(AnonymousRequiredMixin, TemplateView):
    template_name = 'homepage.html'
    authenticated_redirect_url = reverse_lazy(u"booth:recordings-list")


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
