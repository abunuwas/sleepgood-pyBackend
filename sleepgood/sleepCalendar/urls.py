from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from rest_framework.urlpatterns import format_suffix_patterns 

from . import views

app_name = 'sleepCalendar'
urlpatterns = [
    url('^$', views.indexView, name='index'),
    url('^calendar$', views.InsertUpdateDeleteAPI.as_view(), name='insertCalendarEntry'),
    url('calendar/uuid/(?P<uuid>[-\w]+)$', views.GetCalendarEntry.as_view(), name='getCalendarEntryByUuid'),
    url('calendar/year/(?P<date__year>\d+)$', views.GetCalendarEntries.as_view(), name='getCalendarEntriesByYear'),
    #url('^1/calendar$', csrf_exempt(views.InsertUpdateDelete.as_view()), name='insertCalendarEntry'), 
    #url('calendar/year/(?P<year>\d+)$', views.getCalendarEntriesByYear, name='getCalendarEntriesByYear'),
    #url('^(?P<userId>\d+)/calendar/update$', views.InsertUpdate.as_view(), name='updateCalendarEntry'),

    ]

urlpatterns = format_suffix_patterns(urlpatterns)