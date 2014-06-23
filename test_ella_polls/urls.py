try:
    from django.conf.urls import patterns, include
except ImportError:  # Django < 1.4
    from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('',
    (r'^polls', include('ella_polls.urls')),
    (r'^', include('ella.core.urls')),
)
