# Generated by Django 2.2.1 on 2020-05-13 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PropelRapp', '0026_auto_20200513_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roledetail',
            name='submenu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PropelRapp.Submenu'),
        ),
    ]
