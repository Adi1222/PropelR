# Generated by Django 2.2.1 on 2020-05-21 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PropelRapp', '0035_auto_20200521_0721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='roledetail',
            name='submenu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PropelRapp.Submenu'),
        ),
    ]