# Generated by Django 5.1.2 on 2025-02-10 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_cart_quantity_cart_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='booking',
            name='size',
            field=models.CharField(default='1', max_length=50),
            preserve_default=False,
        ),
    ]
