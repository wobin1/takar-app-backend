# Generated by Django 4.2.1 on 2023-06-30 10:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0008_savings_savings_goal'),
    ]

    operations = [
        migrations.AddField(
            model_name='savings',
            name='deadline',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]