# Generated by Django 4.2.1 on 2023-07-02 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alawi', '0003_alawi_amount_to_be_paid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alawi',
            old_name='product_owner',
            new_name='owner_id',
        ),
    ]