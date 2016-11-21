from django.conf.urls import url, include
from rest_framework import routers

from .api import RecordingViewSet
from .views import (RecordingListView, RecordingDetailView, RecordingCreateView,
                    RecordingUpdateView)

router = routers.DefaultRouter()
router.register(r'recording', RecordingViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    url(r'^api/v1/', include(router.urls)),
)

urlpatterns += (
    # urls for Recording
    url(r'^booth/recording/$',
        RecordingListView.as_view(),
        name='booth_recording_list'
    ),
    url(r'^booth/recording/create/$',
        RecordingCreateView.as_view(),
        name='booth_recording_create'
    ),
    url(r'^booth/recording/detail/(?P<id>\S+)/$',
        RecordingDetailView.as_view(),
        name='booth_recording_detail'
    ),
    url(r'^booth/recording/update/(?P<id>\S+)/$',
        RecordingUpdateView.as_view(),
        name='booth_recording_update'
    ),
)

