# Generated by Django 4.2.2 on 2023-08-02 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marks', '0011_alter_acceptedplace_created'),
        ('accountants', '0011_alter_paymentaccepted_accept_mark'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PaymentAccepted',
            new_name='PaymentMark',
        ),
    ]