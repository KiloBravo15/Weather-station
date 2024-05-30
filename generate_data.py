import os
import django
from random import uniform, choice
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_station.settings')
django.setup()

from weather.models import WeatherData

def generate_sample_data(start_date, end_date):
    current_time = start_date

    while current_time <= end_date:
        hour = current_time.hour

        # Temperatura
        if hour == 0:
            temperature = uniform(16, 18)
        elif 1 <= hour < 5:
            temperature -= uniform(0.1, 0.2)  # Powolny spadek w nocy
        elif hour == 5:
            temperature = uniform(14, 15) + uniform(0.1, 0.2)  # Przed godziną minimum
        elif hour == 6:
            temperature = uniform(14, 15)  # Minimum temperatury
        elif hour == 7:
            temperature = uniform(14, 15) + uniform(0.1, 0.2)  # Po godzinie minimum
        elif 8 <= hour < 16:
            temperature += uniform(0.2, 0.5)  # Powolny wzrost w ciągu dnia
        elif hour == 16:
            temperature = uniform(20, 27) - uniform(0.1, 0.2)  # Przed godziną maksimum
        elif hour == 17:
            temperature = uniform(20, 27)  # Maksimum temperatury
        elif hour == 18:
            temperature = uniform(20, 27) - uniform(0.1, 0.2)  # Po godzinie maksimum
        elif 19 <= hour < 20:
            temperature -= uniform(0.1, 0.2)  # Powolny spadek wczesnym wieczorem
        else:
            temperature -= uniform(0.2, 0.5)  # Większy spadek późnym wieczorem

        # Korekta wartości temperatury do realistycznych zakresów
        if hour >= 5 and hour < 16:
            temperature = min(temperature, uniform(20, 27))
        else:
            temperature = max(temperature, uniform(14, 18))

        # Wilgotność
        if hour == 0:
            humidity = uniform(50, 60)
        elif 1 <= hour < 5:
            humidity += uniform(0.5, 1.5)  # Wzrost w nocy
        elif hour == 5:
            humidity = uniform(70, 80) - uniform(1, 2)  # Przed godziną maksimum
        elif hour == 6:
            humidity = uniform(70, 80)  # Maksimum wilgotności
        elif hour == 7:
            humidity = uniform(70, 80) - uniform(1, 2)  # Po godzinie maksimum
        elif 8 <= hour < 9:
            humidity -= uniform(1.0, 2.0)  # Mocny spadek rano
        elif 9 <= hour < 15:
            humidity -= uniform(0.5, 1.0)  # Łagodny spadek w ciągu dnia
        elif hour == 15:
            humidity = uniform(30, 40) + uniform(1, 2)  # Przed godziną minimum
        elif hour == 16:
            humidity = uniform(30, 40)  # Minimum wilgotności
        elif hour == 17:
            humidity = uniform(30, 40) + uniform(1, 2)  # Po godzinie minimum
        elif 18 <= hour < 20:
            humidity += uniform(0.5, 1.0)  # Wzrost po południu
        else:
            humidity += uniform(1.0, 1.5)  # Większy wzrost wieczorem

        # Korekta wartości wilgotności do realistycznych zakresów
        if not (0 <= hour < 6 or 18 <= hour < 24):
            humidity = max(humidity, 30)
            humidity = min(humidity, 60)
        else:
            humidity = max(humidity, 50)
            humidity = min(humidity, 80)

        # Jeśli pada deszcz
        rainfall = choice([False, False, False, True])  # Mniejsze prawdopodobieństwo deszczu
        if rainfall and 17 <= hour < 20:  # Deszcz między 17:00 a 20:00
            temperature -= uniform(0.5, 1.5)
            humidity = 100
            # Zwiększona wilgotność przed i po deszczu
            if hour == 17:
                humidity = min(humidity + 20, 100)
            elif hour == 19:
                humidity = min(humidity - 20, 80)

        light_intensity = uniform(0, 1000)  # Światło w zakresie 0-1000 lux

        WeatherData.objects.create(
            timestamp=current_time,
            temperature=temperature,
            humidity=humidity,
            pressure=uniform(980, 1020),
            rainfall=rainfall,
            light_intensity=light_intensity
        )
        current_time += timedelta(hours=1)

start_date = datetime(2024, 5, 1, 0, 0)
end_date = datetime(2024, 5, 29, 23, 59)

generate_sample_data(start_date, end_date)
