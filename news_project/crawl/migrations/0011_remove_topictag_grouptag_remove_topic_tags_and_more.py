# Generated by Django 5.0.6 on 2024-07-13 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawl', '0010_alter_crawl_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topictag',
            name='grouptag',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='tags',
        ),
        migrations.AlterUniqueTogether(
            name='topictag',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='topictag',
            name='topic',
        ),
        migrations.DeleteModel(
            name='GroupTag',
        ),
        migrations.DeleteModel(
            name='TopicTag',
        ),
    ]
