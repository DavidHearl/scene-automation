# Generated by Django 3.2.21 on 2024-02-19 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0034_auto_20240219_1526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='area',
            name='processing',
        ),
        migrations.AddField(
            model_name='machine',
            name='processing',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='front_end.area'),
        ),
    ]