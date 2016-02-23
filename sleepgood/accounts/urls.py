from django.conf.urls import url

from . import views

app_name = 'accounts'
urlpatterns = [
	url('^register$', views.Register.as_view(), name='register'),
	url('^login$', views.login, name='login'),
	url('^logout', views.logout, name='logout'),
	]