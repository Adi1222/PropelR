# Generated by Django 2.2.1 on 2020-05-13 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0005_auto_20200513_0832'),
        ('auth', '0011_update_proxy_permissions'),
        ('PropelRapp', '0023_auto_20200513_0730'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AppUser',
            new_name='User',
        ),
        migrations.AlterField(
            model_name='roledetail',
            name='submenu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PropelRapp.Submenu'),
        ),
        migrations.AlterModelTable(
            name='user',
            table='User',
        ),
    ]
