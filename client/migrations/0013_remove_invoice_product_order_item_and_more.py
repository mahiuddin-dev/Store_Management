# Generated by Django 4.1.2 on 2022-10-25 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0012_remove_productorderitem_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='product_order_item',
        ),
        migrations.AddField(
            model_name='productorderitem',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.productorder'),
        ),
    ]