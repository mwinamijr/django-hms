# Generated by Django 5.1.4 on 2025-02-07 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='kin_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='kin_phone',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='kin_relation',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='marital_status',
            field=models.CharField(choices=[('single', 'Single'), ('married', 'Married')], default='single', max_length=50),
        ),
        migrations.AddField(
            model_name='patient',
            name='national_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='occupation',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='priority',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='patient',
            name='registration_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
