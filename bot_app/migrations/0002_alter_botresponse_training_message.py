# Generated by Django 5.1.6 on 2025-02-11 20:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botresponse',
            name='training_message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot_app.trainingmessage'),
        ),
    ]
