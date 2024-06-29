# Generated by Django 5.0.6 on 2024-06-25 19:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_reason_alter_news_topic_keyreason'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='keyreason',
            options={'verbose_name_plural': 'Từ khoá nguyên nhân'},
        ),
        migrations.RemoveField(
            model_name='keyreason',
            name='reason',
        ),
        migrations.AddField(
            model_name='keyreason',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reason',
            name='keyreason',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='news.keyreason'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reason',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
