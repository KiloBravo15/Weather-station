# Generated by Django 5.0.6 on 2024-05-29 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weatherdata',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]