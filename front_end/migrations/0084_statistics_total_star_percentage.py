# Generated by Django 3.2.21 on 2024-09-30 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0083_alter_area_min_overlap'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistics',
            name='total_star_percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
