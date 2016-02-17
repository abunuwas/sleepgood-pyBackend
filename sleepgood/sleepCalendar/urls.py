from django.conf.urls import url

from . import views

app_name = 'sleepCalendar'
urlpatterns = [
    url('^$', views.indexView, name='index'),
    url('^(?P<userId>\d+)/calendar$', views.InsertUpdateDelete.as_view(), name='insertCalendarEntry'), 
    url('(?P<userId>\d+)/calendar/year/(?P<year>\d+)$', views.getCalendarEntriesByYear, name='getCalendarEntriesByYear'),
    #url('^(?P<userId>\d+)/calendar/update$', views.InsertUpdate.as_view(), name='updateCalendarEntry'),
    ]