# Generated by Django 4.2.2 on 2023-07-24 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_accountant_supervisor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accountant',
            options={'verbose_name': 'Accountant', 'verbose_name_plural': 'Accountants'},
        ),
        migrations.AlterModelOptions(
            name='supervisor',
            options={'verbose_name': 'Supervisor', 'verbose_name_plural': 'Supervisors'},
        ),
    ]