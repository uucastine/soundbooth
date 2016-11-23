from django.conf.urls import url, include
from rest_framework import routers

from .api import RecordingViewSet, ScheduleViewSet
from .views import (RecordingListView, RecordingDetailView, RecordingCreateView,
                    RecordingUpdateView, ScheduleDetailView, ScheduleCreateView,
                    ScheduleListView, ScheduleUpdateView)

router = routers.DefaultRouter()
router.register(r'recording', RecordingViewSet)
router.register(r'schedule', ScheduleViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    url(r'^api/v1/', include(router.urls)),
)

urlpatterns += (
    # urls for Recording
    url(r'^recordings/$',
        RecordingListView.as_view(),
        name='recording_list'
    ),
    url(r'^recordings/create/$',
        RecordingCreateView.as_view(),
        name='recording-create'
    ),
    url(r'^recordings/detail/(?P<slug>[0-9a-z-]+)/$',
        RecordingDetailView.as_view(),
        name='recording-detail'
    ),
    url(r'^recordings/update/(?P<slug>[0-9a-z-]+)/$',
        RecordingUpdateView.as_view(),
        name='recording-update'
    ),

    url(r'^schedules/$',
        ScheduleListView.as_view(),
        name='schedule-list'
    ),
    url(r'^schedules/create/$',
        ScheduleCreateView.as_view(),
        name='schedule-create'
    ),
    url(r'^schedules/detail/(?P<slug>[0-9a-z-]+)/$',
        ScheduleDetailView.as_view(),
        name='schedule-detail'
    ),
    url(r'^schedules/update/(?P<slug>[0-9a-z-]+)/$',
        ScheduleUpdateView.as_view(),
        name='schedule-update'
    ),
)

