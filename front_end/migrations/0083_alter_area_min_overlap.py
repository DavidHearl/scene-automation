# Generated by Django 3.2.21 on 2024-09-25 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0082_auto_20240925_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='min_overlap',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3),
        ),
    ]
