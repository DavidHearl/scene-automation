# Generated by Django 3.2.21 on 2024-07-22 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0071_booking_ship'),
    ]

    operations = [
        migrations.AddField(
            model_name='ship',
            name='contains_not_required',
            field=models.BooleanField(default=False),
        ),
    ]
