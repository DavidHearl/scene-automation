# Generated by Django 3.2.21 on 2024-04-16 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0043_auto_20240408_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='ship',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
