# Generated by Django 4.1.2 on 2022-10-25 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0011_alter_productorder_installment_pay_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productorderitem',
            name='order',
        ),
    ]
