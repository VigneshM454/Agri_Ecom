# Generated by Django 5.1.1 on 2024-09-14 13:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_customer_alter_cart_userid_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.customer'),
        ),
    ]
