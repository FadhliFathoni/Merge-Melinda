# Generated by Django 4.1.1 on 2023-02-09 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0002_account_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='poin',
        ),
    ]
