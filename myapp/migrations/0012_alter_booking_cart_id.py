# Generated by Django 4.2.9 on 2024-01-31 03:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_booking_cart_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='cart_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.cart'),
        ),
    ]