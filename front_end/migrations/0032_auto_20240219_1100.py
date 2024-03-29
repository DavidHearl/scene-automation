# Generated by Django 3.2.21 on 2024-02-19 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0031_delete_machine'),
    ]

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('Idle', 'Idle'), ('Active', 'Active')], default='Idle', max_length=20)),
                ('cpu', models.CharField(max_length=50)),
                ('cpu_core_count', models.IntegerField()),
                ('cpu_thread_count', models.IntegerField()),
                ('cpu_base_frequency', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cpu_turbo_frequency', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cpu_cache', models.IntegerField()),
                ('cpu_tdp', models.IntegerField()),
                ('cpu_interger_math', models.IntegerField()),
                ('cpu_floating_point_math', models.IntegerField()),
                ('cpu_data_encryption', models.IntegerField()),
                ('cpu_data_compression', models.IntegerField()),
                ('cpu_single_thread', models.IntegerField()),
                ('ram_capacity', models.IntegerField()),
                ('ram_type', models.CharField(max_length=50)),
                ('ram_frequency', models.IntegerField()),
                ('storage_capacity', models.IntegerField()),
                ('storage_read_speed', models.IntegerField()),
                ('storage_write_speed', models.IntegerField()),
                ('gpu', models.CharField(max_length=50)),
                ('gpu_memory', models.IntegerField()),
                ('gpu_pixel_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('gpu_texture_rate', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='area',
            name='processing_machine',
        ),
    ]
