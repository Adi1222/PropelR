# Generated by Django 2.2.1 on 2020-06-08 06:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('PropelRapp', '0037_auto_20200521_0733'),
    ]

    operations = [
        migrations.AddField(
            model_name='cluster',
            name='customer',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.CASCADE, to='PropelRapp.Cust_org'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='roledetail',
            name='submenu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PropelRapp.Submenu'),
        ),
    ]
