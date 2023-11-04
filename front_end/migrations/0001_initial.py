# Generated by Django 3.2 on 2023-10-31 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Ship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('contract_number', models.IntegerField()),
                ('company', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imported', models.BooleanField(default=False)),
                ('processed', models.BooleanField(default=False)),
                ('registered', models.BooleanField(default=False)),
                ('alignment', models.BooleanField(default=False)),
                ('clean', models.BooleanField(default=False)),
                ('point_cloud', models.BooleanField(default=False)),
                ('export', models.BooleanField(default=False)),
                ('upload', models.BooleanField(default=False)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='front_end.area')),
            ],
        ),
        migrations.AddField(
            model_name='area',
            name='ship',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='front_end.ship'),
        ),
    ]
