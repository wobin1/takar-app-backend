# Generated by Django 4.2.1 on 2023-06-07 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_customuser_groups_customuser_user_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='verification_token',
            field=models.CharField(max_length=255, null=True),
        ),
    ]