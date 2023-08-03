# Generated by Django 4.2.2 on 2023-08-02 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marks', '0011_alter_acceptedplace_created'),
        ('accountants', '0009_paymentaccepted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentaccepted',
            name='accept_mark',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='marks.acceptedplace', verbose_name='Mark'),
        ),
    ]