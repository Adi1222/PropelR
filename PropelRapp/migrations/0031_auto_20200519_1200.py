# Generated by Django 2.2.1 on 2020-05-19 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PropelRapp', '0030_auto_20200519_1137'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appuser',
            old_name='image',
            new_name='profile_pic',
        ),
        migrations.AlterField(
            model_name='roledetail',
            name='submenu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PropelRapp.Submenu'),
        ),
    ]
