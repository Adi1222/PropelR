# Generated by Django 2.2.1 on 2020-05-04 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PropelRapp', '0005_auto_20200502_0553'),
    ]

    operations = [
        migrations.CreateModel(
            name='Algo_master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('algo', models.CharField(max_length=30)),
                ('algo_desc', models.CharField(max_length=80)),
                ('is_deleted', models.CharField(choices=[('N', 'NO'), ('Y', 'YES')], default='N', max_length=1)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=20)),
                ('modified_on', models.DateTimeField(auto_now=True, null=True)),
                ('modified_by', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'Algo_master',
                'managed': True,
            },
        ),
    ]
