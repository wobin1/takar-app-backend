# Generated by Django 4.2.1 on 2023-06-21 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_remove_customuser_verification_token_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='verification_token',
            new_name='verifications_token',
        ),
    ]
