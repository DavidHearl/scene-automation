# Generated by Django 3.2.21 on 2024-07-02 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0065_auto_20240701_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistics',
            name='total_stars',
            field=models.IntegerField(default=0),
        ),
    ]
