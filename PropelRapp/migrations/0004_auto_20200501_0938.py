# Generated by Django 2.2.1 on 2020-05-01 09:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('PropelRapp', '0003_auto_20200501_0753'),
    ]

    operations = [
        migrations.AddField(
            model_name='camera',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='camera',
            name='modified_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
