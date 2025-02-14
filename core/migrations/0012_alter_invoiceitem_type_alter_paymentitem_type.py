# Generated by Django 5.1.4 on 2025-02-14 09:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_itemtype_alter_hospitalitem_item_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceitem',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.itemtype'),
        ),
        migrations.AlterField(
            model_name='paymentitem',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.itemtype'),
        ),
    ]
