# Generated by Django 2.2.1 on 2020-05-02 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PropelRapp', '0004_auto_20200501_0938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='camera',
            name='features',
        ),
        migrations.RemoveField(
            model_name='camera',
            name='purpose',
        ),
        migrations.AlterField(
            model_name='camera',
            name='algo_type',
            field=models.CharField(choices=[('Vehicle', 'Vehicle'), ('Person', 'Person')], default='Type', max_length=20),
        ),
    ]
