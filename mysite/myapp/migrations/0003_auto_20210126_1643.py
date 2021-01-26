# Generated by Django 3.1.5 on 2021-01-26 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20210124_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nutrient',
            name='amount',
            field=models.FloatField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='nutrient',
            name='unit',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
