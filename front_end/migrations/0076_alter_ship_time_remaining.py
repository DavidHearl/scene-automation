# Generated by Django 3.2.21 on 2024-08-13 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0075_booking_survey_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ship',
            name='time_remaining',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, null=True),
        ),
    ]
