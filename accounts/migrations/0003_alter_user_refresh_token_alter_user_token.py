# Generated by Django 4.2.2 on 2023-07-16 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_refresh_token_user_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='refresh_token',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.TextField(blank=True, null=True),
        ),
    ]