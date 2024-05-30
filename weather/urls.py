from django.urls import path
from .views import weather_charts_calendar, weather_charts_measurements

urlpatterns = [
    path('', weather_charts_calendar, name='weather_charts_calendar'),
    path('last_measurements/', weather_charts_measurements, name='weather_charts_last_measurements'),
]
