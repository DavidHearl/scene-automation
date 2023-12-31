# Generated by Django 3.2.21 on 2023-11-23 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0019_auto_20231121_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='priority',
            field=models.IntegerField(choices=[(0, 'Priority 0'), (1, 'Priority 1'), (2, 'Priority 2'), (3, 'Priority 3')], default=0),
        ),
        migrations.AlterField(
            model_name='area',
            name='aligned',
            field=models.CharField(choices=[('No Data', 'No Data'), ('Legacy', 'Legacy'), ('Minor Fail', 'Minor Fail'), ('Major Fail', 'Major Fail'), ('Critical Fail', 'Critical Fail'), ('Queued', 'Queued'), ('WIP', 'WIP'), ('Completed', 'Completed')], default='Completed', max_length=20),
        ),
        migrations.AlterField(
            model_name='area',
            name='cleaned',
            field=models.CharField(choices=[('No Data', 'No Data'), ('Legacy', 'Legacy'), ('Minor Fail', 'Minor Fail'), ('Major Fail', 'Major Fail'), ('Critical Fail', 'Critical Fail'), ('Queued', 'Queued'), ('WIP', 'WIP'), ('Completed', 'Completed')], default='Completed', max_length=20),
        ),
        migrations.AlterField(
            model_name='area',
            name='exported',
            field=models.CharField(choices=[('No Data', 'No Data'), ('Legacy', 'Legacy'), ('Minor Fail', 'Minor Fail'), ('Major Fail', 'Major Fail'), ('Critical Fail', 'Critical Fail'), ('Queued', 'Queued'), ('WIP', 'WIP'), ('Completed', 'Completed')], default='Completed', max_length=20),
        ),
        migrations.AlterField(
            model_name='area',
            name='imported',
            field=models.CharField(choices=[('No Data', 'No Data'), ('Legacy', 'Legacy'), ('Minor Fail', 'Minor Fail'), ('Major Fail', 'Major Fail'), ('Critical Fail', 'Critical Fail'), ('Queued', 'Queued'), ('WIP', 'WIP'), ('Completed', 'Completed')], default='Completed', max_length=20),
        ),
        migrations.AlterField(
            model_name='area',
            name='point_cloud',
            field=models.CharField(choices=[('No Data', 'No Data'), ('Legacy', 'Legacy'), ('Minor Fail', 'Minor Fail'), ('Major Fail', 'Major Fail'), ('Critical Fail', 'Critical Fail'), ('Queued', 'Queued'), ('WIP', 'WIP'), ('Completed', 'Completed')], default='Completed', max_length=20),
        ),
        migrations.AlterField(
            model_name='area',
            name='processed',
            field=models.CharField(choices=[('No Data', 'No Data'), ('Legacy', 'Legacy'), ('Minor Fail', 'Minor Fail'), ('Major Fail', 'Major Fail'), ('Critical Fail', 'Critical Fail'), ('Queued', 'Queued'), ('WIP', 'WIP'), ('Completed', 'Completed')], default='Completed', max_length=20),
        ),
        migrations.AlterField(
            model_name='area',
            name='registered',
            field=models.CharField(choices=[('No Data', 'No Data'), ('Legacy', 'Legacy'), ('Minor Fail', 'Minor Fail'), ('Major Fail', 'Major Fail'), ('Critical Fail', 'Critical Fail'), ('Queued', 'Queued'), ('WIP', 'WIP'), ('Completed', 'Completed')], default='Completed', max_length=20),
        ),
        migrations.AlterField(
            model_name='area',
            name='uploaded',
            field=models.CharField(choices=[('No Data', 'No Data'), ('Legacy', 'Legacy'), ('Minor Fail', 'Minor Fail'), ('Major Fail', 'Major Fail'), ('Critical Fail', 'Critical Fail'), ('Queued', 'Queued'), ('WIP', 'WIP'), ('Completed', 'Completed')], default='Completed', max_length=20),
        ),
    ]
