# Generated by Django 5.0.6 on 2024-06-22 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawl', '0006_topic_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crawl',
            name='is_collecteds',
        ),
        migrations.AddField(
            model_name='crawl',
            name='is_extract',
            field=models.BooleanField(default=True),
        ),
    ]
