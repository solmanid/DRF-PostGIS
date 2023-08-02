# Generated by Django 4.2.2 on 2023-08-02 08:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marks', '0011_alter_acceptedplace_created'),
        ('accountants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Price')),
                ('accept_mark', models.ManyToManyField(to='marks.acceptedplace', verbose_name='Mark')),
                ('accountant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountants.accountant', verbose_name='Accountant')),
            ],
        ),
    ]
