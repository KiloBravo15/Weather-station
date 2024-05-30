from django.db import models

class WeatherData(models.Model):
    timestamp = models.DateTimeField()
    temperature = models.FloatField()  # SHT40
    humidity = models.FloatField()     # SHT40
    pressure = models.FloatField()     # MPL115A2
    rainfall = models.BooleanField()   # YL-83 (bool indicating if it is raining)
    light_intensity = models.FloatField()  # BH1750

    def __str__(self):
        return (
            f"{self.timestamp} - Temp: {self.temperature}, Hum: {self.humidity}, "
            f"Pres: {self.pressure}, Rainfall: {self.rainfall}, Light Intensity: {self.light_intensity}"
        )
