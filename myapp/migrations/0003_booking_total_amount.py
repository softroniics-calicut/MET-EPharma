# Generated by Django 4.2.9 on 2024-01-25 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_product_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='total_amount',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]