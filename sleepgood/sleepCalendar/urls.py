from django.conf.urls import url

from . import views

app_name = 'sleepCalendar'
urlpatterns = [
    url('^$', views.indexView, name='index'),
    ]