# Generated by Django 3.2 on 2023-10-31 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0004_auto_20231031_1452'),
    ]

    operations = [
        migrations.RenameField(
            model_name='status',
            old_name='area',
            new_name='area_name',
        ),
    ]