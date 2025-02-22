# Generated by Django 5.1.4 on 2025-02-08 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_patient_is_active_patient_kin_name_patient_kin_phone_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='patient',
            options={'ordering': ('patient_number',)},
        ),
        migrations.AddField(
            model_name='patient',
            name='patient_number',
            field=models.CharField(blank=True, max_length=9, null=True, unique=True),
        ),
    ]
