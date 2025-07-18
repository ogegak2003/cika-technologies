# Generated by Django 5.2.4 on 2025-07-12 14:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booking',
            options={'ordering': ['-booking_date'], 'verbose_name_plural': 'Bookings'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ['name'], 'verbose_name_plural': 'Services'},
        ),
        migrations.AlterModelOptions(
            name='servicecategory',
            options={'ordering': ['name'], 'verbose_name_plural': 'Service Categories'},
        ),
        migrations.AddField(
            model_name='service',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
        migrations.AddField(
            model_name='servicecategory',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='services.service'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='services.servicecategory'),
        ),
        migrations.AlterField(
            model_name='service',
            name='duration',
            field=models.PositiveIntegerField(help_text='Duration in minutes'),
        ),
        migrations.AlterField(
            model_name='servicecategory',
            name='icon',
            field=models.CharField(blank=True, default='gear', max_length=50),
        ),
        migrations.AlterField(
            model_name='servicecategory',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
