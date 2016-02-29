from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'accounts'
urlpatterns = [
	url('^register$', csrf_exempt(views.Register.as_view()), name='register'),
	url('^login$', views.login, name='login'),
	url('^logout$', views.logout, name='logout'),
	url('^expose$', views.expose, name='expose'),
	]