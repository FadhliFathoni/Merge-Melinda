# Generated by Django 4.1.1 on 2023-02-13 00:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Transaction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaksi',
            name='waktuTransaksi',
            field=models.TextField(default=datetime.date(2023, 2, 13)),
        ),
    ]
