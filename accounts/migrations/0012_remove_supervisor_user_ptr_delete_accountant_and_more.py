# Generated by Django 4.2.2 on 2023-07-25 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_accountant_accountant_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supervisor',
            name='user_ptr',
        ),
        migrations.DeleteModel(
            name='Accountant',
        ),
        migrations.DeleteModel(
            name='Supervisor',
        ),
    ]