# Generated by Django 3.2 on 2023-10-31 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0007_auto_20231031_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='alignment',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='status',
            name='clean',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='status',
            name='exported',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='status',
            name='imported',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='status',
            name='point_cloud',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='status',
            name='processed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='status',
            name='registered',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='status',
            name='uploaded',
            field=models.BooleanField(default=False),
        ),
    ]