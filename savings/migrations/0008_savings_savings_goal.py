# Generated by Django 4.2.1 on 2023-06-30 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0007_alter_savings_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='savings',
            name='savings_goal',
            field=models.IntegerField(default=0),
        ),
    ]