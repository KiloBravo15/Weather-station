from django.shortcuts import render
from .models import WeatherData
from django.utils import timezone
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO
import base64
import urllib.parse
import matplotlib.dates as mdates

def get_weekly_data(start_date, end_date):
    data = WeatherData.objects.filter(timestamp__range=[start_date, end_date + timedelta(days=1)])
    df = pd.DataFrame(list(data.values('timestamp', 'temperature', 'humidity', 'pressure', 'light_intensity', 'rainfall')))
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    return df

def plot_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
    return uri

def current_weather():
    # Get the latest weather data entry
    latest_weather = WeatherData.objects.latest('timestamp')

    # Determine weather condition based on rainfall and light intensity
    if latest_weather.rainfall:
        weather_condition = 'Rainy'
    elif latest_weather.light_intensity < 300:
        weather_condition = 'Cloudy'
    elif latest_weather.light_intensity < 700:
        weather_condition = 'Partly Cloudy'
    else:
        weather_condition = 'Sunny'

    # Preprocess data
    temperature = round(latest_weather.temperature, 1)
    humidity = round(latest_weather.humidity)
    pressure = round(latest_weather.pressure)

    context = {
        'weather_condition': weather_condition,
        'temperature': temperature,
        'humidity': humidity,
        'pressure': pressure,
        'timestamp': latest_weather.timestamp,
    }

    return context

def weather_charts_calendar(request):
    today = timezone.localtime()
    last_monday = today - timedelta(days=today.weekday() + 7)
    last_sunday = last_monday + timedelta(days=6)
    may_start = timezone.make_aware(datetime(today.year, 5, 1), timezone.get_current_timezone())

    if request.method == 'GET':
        start_date_str = request.GET.get('start_date', last_monday.strftime('%Y-%m-%d'))
        end_date_str = request.GET.get('end_date', last_sunday.strftime('%Y-%m-%d'))
        start_date = timezone.make_aware(datetime.strptime(start_date_str, '%Y-%m-%d'))
        end_date = timezone.make_aware(datetime.strptime(end_date_str, '%Y-%m-%d'))
    else:
        start_date = timezone.make_aware(last_monday)
        end_date = timezone.make_aware(last_sunday)

    # Walidacja dat
    if start_date < may_start:
        start_date = may_start
    if end_date > today:
        end_date = today
    if end_date < start_date:
        end_date = start_date

    df = get_weekly_data(start_date, end_date)
    
    if df.empty:
        context = {
            'error': 'No data found for the given date range.',
            'start_date': start_date_str,
            'end_date': end_date_str,
            'today': today.date().strftime('%Y-%m-%d')
        }
        return render(request, 'weather_charts.html', context)
    
    # Calculate summary statistics
    summary_stats = {
        'temperature': {
            'max': df['temperature'].max(),
            'min': df['temperature'].min(),
            'mean': df['temperature'].mean()
        },
        'humidity': {
            'max': df['humidity'].max(),
            'min': df['humidity'].min(),
            'mean': df['humidity'].mean()
        },
        'pressure': {
            'max': df['pressure'].max(),
            'min': df['pressure'].min(),
            'mean': df['pressure'].mean()
        },
        'light_intensity': {
            'max': df['light_intensity'].max(),
            'min': df['light_intensity'].min(),
            'mean': df['light_intensity'].mean()
        },
        'rainfall': {
            'rainy_hours': df['rainfall'].sum(),
            'dry_hours': len(df) - df['rainfall'].sum()
        }
    }

    # Create temperature plot
    fig_temp, ax_temp = plt.subplots(figsize=(12, 5))
    df['temperature'].plot(ax=ax_temp, color='red', label='Temperature')
    ax_temp.set_ylabel('Temperature (°C)')
    ax_temp.grid(True)
    ax_temp.legend(loc='lower left', bbox_to_anchor=(0, 1.02), ncol=1, frameon=False, borderaxespad=0, handletextpad=0)
    temp_plot = plot_to_base64(fig_temp)
    plt.close(fig_temp)

    # Create humidity plot
    fig_hum, ax_hum = plt.subplots(figsize=(12, 5))
    df['humidity'].plot(ax=ax_hum, color='blue', label='Humidity')
    ax_hum.set_ylabel('Humidity (%)')
    ax_hum.grid(True)
    ax_hum.legend(loc='lower left', bbox_to_anchor=(0, 1.02), ncol=1, frameon=False, borderaxespad=0, handletextpad=0)
    hum_plot = plot_to_base64(fig_hum)
    plt.close(fig_hum)

    # Create pressure plot
    fig_pres, ax_pres = plt.subplots(figsize=(12, 5))
    df['pressure'].plot(ax=ax_pres, color='green', label='Pressure')
    ax_pres.set_ylabel('Pressure (hPa)')
    ax_pres.grid(True)
    ax_pres.legend(loc='lower left', bbox_to_anchor=(0, 1.02), ncol=1, frameon=False, borderaxespad=0, handletextpad=0)
    pres_plot = plot_to_base64(fig_pres)
    plt.close(fig_pres)

    # Create light intensity plot
    fig_light, ax_light = plt.subplots(figsize=(12, 5))
    df['light_intensity'].plot(ax=ax_light, color='orange', label='Light Intensity')
    ax_light.set_ylabel('Light Intensity (lux)')
    ax_light.grid(True)
    ax_light.legend(loc='lower left', bbox_to_anchor=(0, 1.02), ncol=1, frameon=False, borderaxespad=0, handletextpad=0)
    light_plot = plot_to_base64(fig_light)
    plt.close(fig_light)

    # Create rainfall plot
    fig_rain, ax_rain = plt.subplots(figsize=(12, 3))
    ax_rain.scatter(df.index, df['rainfall'].astype(int), color='blue', label='Rainfall')
    ax_rain.set_ylabel('Rainfall (0 or 1)')
    ax_rain.set_ylim(-0.3, 1.3)
    ax_rain.set_yticks([0, 1])
    ax_rain.set_yticklabels(['0', '1'])
    ax_rain.grid(True)
    ax_rain.legend(loc='lower left', bbox_to_anchor=(0, 1.02), ncol=1, frameon=False, borderaxespad=0, handletextpad=0)
    rain_plot = plot_to_base64(fig_rain)
    plt.close(fig_rain)

    current_weather_context = current_weather()
    context = {
        'temp_plot': temp_plot,
        'hum_plot': hum_plot,
        'pres_plot': pres_plot,
        'light_plot': light_plot,
        'rain_plot': rain_plot,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'today': today.date().strftime('%Y-%m-%d'),
        'summary_stats': summary_stats,
    }
    context.update(current_weather_context)

    return render(request, 'weather_charts_calendar.html', context)

def weather_charts_measurements(request):
    today = timezone.localtime()
    
    # Take 10 last measurements
    data = WeatherData.objects.order_by('-timestamp')[:10]
    df = pd.DataFrame(list(data.values('timestamp', 'temperature', 'humidity', 'pressure', 'light_intensity', 'rainfall')))
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    
    if df.empty:
        context = {
            'error': 'No data found.',
            'today': today.date().strftime('%Y-%m-%d')
        }
        return render(request, 'weather_charts_last_measurements.html', context)
    
    # Calculate summary statistics
    summary_stats = {
        'temperature': {
            'max': df['temperature'].max(),
            'min': df['temperature'].min(),
            'mean': df['temperature'].mean()
        },
        'humidity': {
            'max': df['humidity'].max(),
            'min': df['humidity'].min(),
            'mean': df['humidity'].mean()
        },
        'pressure': {
            'max': df['pressure'].max(),
            'min': df['pressure'].min(),
            'mean': df['pressure'].mean()
        },
        'light_intensity': {
            'max': df['light_intensity'].max(),
            'min': df['light_intensity'].min(),
            'mean': df['light_intensity'].mean()
        },
        'rainfall': {
            'rainy_hours': df['rainfall'].sum(),
            'dry_hours': len(df) - df['rainfall'].sum()
        }
    }

    # Create temperature plot
    fig_temp, ax_temp = plt.subplots(figsize=(12, 5))
    df['temperature'].plot(ax=ax_temp, color='red', label='Temperature', marker='o')
    ax_temp.set_ylabel('Temperature (°C)')
    ax_temp.grid(True)
    ax_temp.legend(loc='lower left', bbox_to_anchor=(0, 1.02), ncol=1, frameon=False, borderaxespad=0, handletextpad=0)
    temp_plot = plot_to_base64(fig_temp)
    plt.close(fig_temp)

    # Create humidity plot
    fig_hum, ax_hum = plt.subplots(figsize=(12, 5))
    df['humidity'].plot(ax=ax_hum, color='blue', label='Humidity', marker='o')
    ax_hum.set_ylabel('Humidity (%)')
    ax_hum.grid(True)
    ax_hum.legend(loc='lower left', bbox_to_anchor=(0, 1.02), ncol=1, frameon=False, borderaxespad=0, handletextpad=0)
    hum_plot = plot_to_base64(fig_hum)
    plt.close(fig_hum)

    # Create pressure plot
    fig_pres, ax_pres = plt.subplots(figsize=(12, 5))
    df['pressure'].plot(ax=ax_pres, color='green', label='Pressure', marker='o')
    ax_pres.set_ylabel('Pressure (hPa)')
    ax_pres.grid(True)
    ax_pres.legend(loc='lower left', bbox_to_anchor=(0, 1.02), ncol=1, frameon=False, borderaxespad=0, handletextpad=0)
    pres_plot = plot_to_base64(fig_pres)
    plt.close(fig_pres)

    # Create light intensity plot
    fig_light, ax_light = plt.subplots(figsize=(12, 5))
    df['light_intensity'].plot(ax=ax_light, color='orange', label='Light Intensity', marker='o')
    ax_light.set_ylabel('Light Intensity (lux)')
    ax_light.grid(True)
    ax_light.legend(loc='lower left', bbox_to_anchor=(0, 1.02), ncol=1, frameon=False, borderaxespad=0, handletextpad=0)
    light_plot = plot_to_base64(fig_light)
    plt.close(fig_light)

    # Create rainfall plot
    fig_rain, ax_rain = plt.subplots(figsize=(12, 3))
    ax_rain.scatter(df.index, df['rainfall'].astype(int), color='blue', label='Rainfall')
    ax_rain.set_ylabel('Rainfall (0 or 1)')
    ax_rain.set_ylim(-0.3, 1.3)
    ax_rain.set_yticks([0, 1])
    ax_rain.set_yticklabels(['0', '1'])
    ax_rain.grid(True)
    ax_rain.legend(loc='lower left', bbox_to_anchor=(0, 1.02), ncol=1, frameon=False, borderaxespad=0, handletextpad=0)
    rain_plot = plot_to_base64(fig_rain)
    plt.close(fig_rain)

    current_weather_context = current_weather()
    context = {
        'temp_plot': temp_plot,
        'hum_plot': hum_plot,
        'pres_plot': pres_plot,
        'light_plot': light_plot,
        'rain_plot': rain_plot,
        'today': today.date().strftime('%Y-%m-%d'),
        'summary_stats': summary_stats,
        'view': 'last_measurements'
    }
    context.update(current_weather_context)

    return render(request, 'weather_charts_last_measurements.html', context)
