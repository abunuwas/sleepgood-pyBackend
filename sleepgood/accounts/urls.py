from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'accounts'
urlpatterns = [
	url('^session$', views.Sessions.as_view()),
	url('^user$', csrf_exempt(views.User.as_view()))
]