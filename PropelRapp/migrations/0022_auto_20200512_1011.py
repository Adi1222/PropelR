# Generated by Django 2.2.1 on 2020-05-12 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PropelRapp', '0021_auto_20200512_0941'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='is_deleted',
            field=models.CharField(choices=[('N', 'NO'), ('Y', 'YES')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='roledetail',
            name='submenu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PropelRapp.Submenu'),
        ),
    ]
