# Generated by Django 4.2.1 on 2023-07-04 22:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('transaction_history', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='transaction_id',
        ),
        migrations.AddField(
            model_name='history',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
