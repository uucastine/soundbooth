from django.conf import settings
from django.conf.urls import include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from booth.views import HomepageView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('booth.urls', namespace='booth')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url("^$", HomepageView.as_view(), name="homepage")
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
