# Generated by Django 3.2 on 2023-10-31 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0014_auto_20231031_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='aligned',
            field=models.BooleanField(choices=[('No Data', 'No Data'), ('Legacy', 'Legacy'), ('Failed', 'Failed'), ('Queued', 'Queued'), ('WIP', 'WIP'), ('Completed', 'Completed')], default='No Data', max_length=20),
        ),
        migrations.AlterField(
            model_name='status',
            name='cleaned',
            field=models.BooleanField(choices=[('No Data', 'No Data'), ('Legacy', 'Legacy'), ('Failed', 'Failed'), ('Queued', 'Queued'), ('WIP', 'WIP'), ('Completed', 'Completed')], default='No Data', max_length=20),
        ),
        migrations.AlterField(
            model_name='status',
            name='exported',
            field=models.BooleanField(choices=[('No Data', 'No Data'), ('Legacy', 'Legacy'), ('Failed', 'Failed'), ('Queued', 'Queued'), ('WIP', 'WIP'), ('Completed', 'Completed')], default='No Data', max_length=20),
        ),
        migrations.AlterField(
            model_name='status',
            name='imported',
            field=models.BooleanField(choices=[('No Data', 'No Data'), ('Legacy', 'Legacy'), ('Failed', 'Failed'), ('Queued', 'Queued'), ('WIP', 'WIP'), ('Completed', 'Completed')], default='No Data', max_length=20),
        ),
        migrations.AlterField(
            model_name='status',
            name='point_cloud',
            field=models.BooleanField(choices=[('No Data', 'No Data'), ('Legacy', 'Legacy'), ('Failed', 'Failed'), ('Queued', 'Queued'), ('WIP', 'WIP'), ('Completed', 'Completed')], default='No Data', max_length=20),
        ),
        migrations.AlterField(
            model_name='status',
            name='processed',
            field=models.BooleanField(choices=[('No Data', 'No Data'), ('Legacy', 'Legacy'), ('Failed', 'Failed'), ('Queued', 'Queued'), ('WIP', 'WIP'), ('Completed', 'Completed')], default='No Data', max_length=20),
        ),
        migrations.AlterField(
            model_name='status',
            name='registered',
            field=models.BooleanField(choices=[('No Data', 'No Data'), ('Legacy', 'Legacy'), ('Failed', 'Failed'), ('Queued', 'Queued'), ('WIP', 'WIP'), ('Completed', 'Completed')], default='No Data', max_length=20),
        ),
        migrations.AlterField(
            model_name='status',
            name='uploaded',
            field=models.BooleanField(choices=[('No Data', 'No Data'), ('Legacy', 'Legacy'), ('Failed', 'Failed'), ('Queued', 'Queued'), ('WIP', 'WIP'), ('Completed', 'Completed')], default='No Data', max_length=20),
        ),
    ]
