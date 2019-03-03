from django.conf.urls import url
from mainapp import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.barber_login, name='barber_login'),
]
