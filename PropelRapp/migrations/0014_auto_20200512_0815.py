# Generated by Django 2.2.1 on 2020-05-12 08:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('PropelRapp', '0013_auto_20200512_0802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appuser',
            name='email',
        ),
        migrations.RemoveField(
            model_name='appuser',
            name='password',
        ),
        migrations.RemoveField(
            model_name='appuser',
            name='username',
        ),
        migrations.AddField(
            model_name='appuser',
            name='user',
            field=models.OneToOneField(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='roledetail',
            name='submenu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PropelRapp.Submenu'),
        ),
    ]
