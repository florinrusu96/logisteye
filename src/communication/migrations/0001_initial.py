# Generated by Django 3.1.3 on 2020-11-07 01:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rest_api', '0002_auto_20201106_2349'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instance_url', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest_api.company')),
            ],
        ),
    ]
