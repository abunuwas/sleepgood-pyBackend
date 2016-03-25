from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'sleepCalendar'
urlpatterns = [
    url('^$', views.indexView, name='index'),
    url('^1/calendar$', csrf_exempt(views.InsertUpdateDelete.as_view()), name='insertCalendarEntry'), 
    url('calendar/year/(?P<year>\d+)$', views.getCalendarEntriesByYear, name='getCalendarEntriesByYear'),
    #url('^(?P<userId>\d+)/calendar/update$', views.InsertUpdate.as_view(), name='updateCalendarEntry'),
    ]