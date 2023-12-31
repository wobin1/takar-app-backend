# Generated by Django 4.2.1 on 2023-07-01 23:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('transaction_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('transaction_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('transaction_type', models.CharField(max_length=255)),
                ('transaction_amount', models.FloatField()),
                ('transaction_description', models.TextField()),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
