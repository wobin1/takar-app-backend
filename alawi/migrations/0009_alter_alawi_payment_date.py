# Generated by Django 4.2.1 on 2023-09-18 10:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('alawi', '0008_alter_alawi_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alawi',
            name='payment_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
