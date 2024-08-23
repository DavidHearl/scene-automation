# Generated by Django 3.2.21 on 2024-08-23 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0079_auto_20240821_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='contract_manager',
        ),
        migrations.AddField(
            model_name='booking',
            name='contract_manager',
            field=models.ManyToManyField(blank=True, null=True, related_name='contract_manager', to='front_end.ContractManager'),
        ),
        migrations.RemoveField(
            model_name='booking',
            name='designer',
        ),
        migrations.AddField(
            model_name='booking',
            name='designer',
            field=models.ManyToManyField(blank=True, null=True, related_name='designer', to='front_end.Designer'),
        ),
    ]