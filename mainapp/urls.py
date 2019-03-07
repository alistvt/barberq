from django.conf.urls import url
from mainapp import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.barber_login, name='barber_login'),
    url(r'^logout/$', views.barber_logout, name='barber_logout'),
    url(r'^profile/$', views.barber_profile, name='barber_profile'),
    url(r'^reserves/$', views.view_reserves, name='view_reserves'),
    url(r'^addslot/$', views.add_slot, name='add_slot'),
    url(r'^manageslots/$', views.manage_slots, name='manage_slots'),
]
