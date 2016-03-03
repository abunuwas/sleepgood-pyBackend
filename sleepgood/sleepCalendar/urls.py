from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns 

from . import views

app_name = 'sleepCalendar'
urlpatterns = [
    url('^$', views.indexView, name='index'),
    url('^calendar$', views.InsertUpdateDeleteAPI.as_view(), name='insertCalendarEntry'), 
    url('calendar/year/(?P<year>\d+)$', views.GetCalendarEntries.as_view(), name='getCalendarEntriesByYear'),
    #url('^(?P<userId>\d+)/calendar/update$', views.InsertUpdate.as_view(), name='updateCalendarEntry'),

    ]

urlpatterns = format_suffix_patterns(urlpatterns)