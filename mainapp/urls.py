from django.conf.urls import url
from mainapp import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
]
