# Generated by Django 4.2.2 on 2023-08-01 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marks', '0005_alter_acceptedplace_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='acceptedplace',
            name='action',
            field=models.SmallIntegerField(choices=[('1', 'Accepted'), ('2', 'Failed')], default='1', verbose_name='accept or failed'),
        ),
    ]
