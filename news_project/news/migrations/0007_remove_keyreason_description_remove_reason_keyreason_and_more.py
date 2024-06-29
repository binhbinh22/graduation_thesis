# Generated by Django 5.0.6 on 2024-06-25 19:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_alter_keyreason_options_remove_keyreason_reason_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keyreason',
            name='description',
        ),
        migrations.RemoveField(
            model_name='reason',
            name='keyreason',
        ),
        migrations.AddField(
            model_name='keyreason',
            name='reason',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='news.reason'),
            preserve_default=False,
        ),
    ]