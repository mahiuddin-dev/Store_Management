# Generated by Django 4.1.2 on 2022-10-24 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0006_productorder_total_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='productorder',
            name='unique_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]