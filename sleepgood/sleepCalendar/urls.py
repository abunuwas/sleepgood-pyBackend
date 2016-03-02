from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns 

from . import views

app_name = 'sleepCalendar'
urlpatterns = [
    url('^$', views.indexView, name='index'),
    url('^calendar$', views.InsertUpdateDelete.as_view(), name='insertCalendarEntry'), 
    url('calendar/year/(?P<year>\d+)$', views.getCalendarEntriesByYear, name='getCalendarEntriesByYear'),
    url('rest/(?P<userId>\d+)/calendario/year/(?P<year>\d+)$', views.get_calendar_entries_api, name='getCalendarEntryAPI'),
    #url('^(?P<userId>\d+)/calendar/update$', views.InsertUpdate.as_view(), name='updateCalendarEntry'),

    ]

urlpatterns = format_suffix_patterns(urlpatterns)