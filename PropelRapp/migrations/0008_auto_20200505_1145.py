# Generated by Django 2.2.1 on 2020-05-05 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PropelRapp', '0007_superadmin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cust_org',
            name='onboard_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
