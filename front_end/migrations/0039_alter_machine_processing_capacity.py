# Generated by Django 3.2.21 on 2024-02-19 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0038_machine_processing_capacity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='processing_capacity',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
    ]
