# Generated by Django 3.2 on 2023-10-31 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0013_auto_20231031_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='aligned',
            field=models.BooleanField(choices=[('nodata', 'No Data'), ('legacy', 'Legacy'), ('failed', 'Failed'), ('queued', 'Queued'), ('wip', 'Work In Progress'), ('completed', 'Completed')], default='nodata', max_length=20),
        ),
        migrations.AlterField(
            model_name='status',
            name='cleaned',
            field=models.BooleanField(choices=[('nodata', 'No Data'), ('legacy', 'Legacy'), ('failed', 'Failed'), ('queued', 'Queued'), ('wip', 'Work In Progress'), ('completed', 'Completed')], default='nodata', max_length=20),
        ),
        migrations.AlterField(
            model_name='status',
            name='exported',
            field=models.BooleanField(choices=[('nodata', 'No Data'), ('legacy', 'Legacy'), ('failed', 'Failed'), ('queued', 'Queued'), ('wip', 'Work In Progress'), ('completed', 'Completed')], default='nodata', max_length=20),
        ),
        migrations.AlterField(
            model_name='status',
            name='imported',
            field=models.BooleanField(choices=[('nodata', 'No Data'), ('legacy', 'Legacy'), ('failed', 'Failed'), ('queued', 'Queued'), ('wip', 'Work In Progress'), ('completed', 'Completed')], default='nodata', max_length=20),
        ),
        migrations.AlterField(
            model_name='status',
            name='point_cloud',
            field=models.BooleanField(choices=[('nodata', 'No Data'), ('legacy', 'Legacy'), ('failed', 'Failed'), ('queued', 'Queued'), ('wip', 'Work In Progress'), ('completed', 'Completed')], default='nodata', max_length=20),
        ),
        migrations.AlterField(
            model_name='status',
            name='processed',
            field=models.BooleanField(choices=[('nodata', 'No Data'), ('legacy', 'Legacy'), ('failed', 'Failed'), ('queued', 'Queued'), ('wip', 'Work In Progress'), ('completed', 'Completed')], default='nodata', max_length=20),
        ),
        migrations.AlterField(
            model_name='status',
            name='registered',
            field=models.BooleanField(choices=[('nodata', 'No Data'), ('legacy', 'Legacy'), ('failed', 'Failed'), ('queued', 'Queued'), ('wip', 'Work In Progress'), ('completed', 'Completed')], default='nodata', max_length=20),
        ),
        migrations.AlterField(
            model_name='status',
            name='uploaded',
            field=models.BooleanField(choices=[('nodata', 'No Data'), ('legacy', 'Legacy'), ('failed', 'Failed'), ('queued', 'Queued'), ('wip', 'Work In Progress'), ('completed', 'Completed')], default='nodata', max_length=20),
        ),
    ]
