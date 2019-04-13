from django.conf.urls import url
from mainapp import views
from mainapp.views import api

urlpatterns = [
    url(r'^barbers/$', views.home, name='home'),
    url(r'^barbers/login/$', views.barber_login, name='barber_login'),
    url(r'^barbers/logout/$', views.barber_logout, name='barber_logout'),
    url(r'^barbers/profile/$', views.barber_profile, name='barber_profile'),
    url(r'^barbers/reserves/$', views.view_reserves, name='view_reserves'),
    url(r'^barbers/addslot/$', views.add_slot, name='add_slot'),
    url(r'^barbers/manageslots/$', views.manage_slots, name='manage_slots'),

    url(r'^api/barbers/list/$', api.BarberyListView.as_view(), name='barber_list'),
    url(r'^api/barbers/profile/$', api.BarberyListView.as_view(), name='barber_list'),

]
