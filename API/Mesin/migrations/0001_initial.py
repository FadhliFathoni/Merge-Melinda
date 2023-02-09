# Generated by Django 4.1.1 on 2023-02-09 01:19

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mesin',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=64)),
                ('kapasitas', models.IntegerField()),
                ('terisi', models.IntegerField()),
                ('lokasi', models.TextField(max_length=128, unique=True)),
                ('origin', models.TextField(max_length=128, unique=True)),
                ('id_pengguna_aktif', models.CharField(blank=True, default='', max_length=128)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
            ],
        ),
    ]
