# Generated by Django 3.2.21 on 2024-08-23 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0080_auto_20240823_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='contract_manager',
            field=models.ManyToManyField(blank=True, related_name='contract_manager', to='front_end.ContractManager'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='designer',
            field=models.ManyToManyField(blank=True, related_name='designer', to='front_end.Designer'),
        ),
    ]
