# Generated by Django 4.2.15 on 2024-08-24 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0001_initial'),
        ('Transactions', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Transactions',
            new_name='Transaction',
        ),
    ]
