# Generated by Django 3.2.21 on 2024-07-04 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0067_area_star'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistics',
            name='total_exported_storage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='statistics',
            name='total_processed_storage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='statistics',
            name='total_raw_storage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
