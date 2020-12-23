from django.urls import path

from . import views


app_name = 'taxi'

urlpatterns = [
    path('', views.TripView.as_view({'get': 'list'}), name='trip_list'),
    path('<uuid:trip_id>/', views.TripView.as_view(
        {'get': 'retrieve'}), name='trip_detail'),
]
