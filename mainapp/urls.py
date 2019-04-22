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
    url(r'^api/barbers/profile/(?P<pk>\d+)/$', api.BarberyProfileView.as_view(), name='barber_profile'),
    url(r'^api/barbers/timeslots/(?P<pk>\d+)/$', api.BarberyTimeSlotsListView.as_view(), name='barber_timeslots'),

    url(r'^api/user/signup/$', api.UserSignUpView.as_view(), name='user_signup'),
    url(r'^api/user/password/$', api.UserChangePasswordView.as_view(), name='user_change_password'),
    url(r'^api/user/$', api.UserActionsView.as_view(), name='user_actions'),
    url(r'^api/user/reservations/$', api.UserReservationsView.as_view(), name='user_reservations'),
    url(r'^api/user/reserve/(?P<pk>\d+)/$', api.UserReserveTimeSlotView.as_view(), name='user_reserve'),
    url(r'^api/user/unreserve/(?P<pk>\d+)/$', api.UserCancelReservationView.as_view(), name='user_cancel_reserve'),
    url(r'^api/user/slots/$', api.UserViewTimeSlots.as_view(), name='user_view_slots'),
]
