# Generated by Django 3.1.3 on 2020-11-07 03:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rest_api', '0004_auto_20201107_0255'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instance_url', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('is_master_instance', models.BooleanField(default=False, editable=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest_api.company')),
            ],
        ),
    ]
