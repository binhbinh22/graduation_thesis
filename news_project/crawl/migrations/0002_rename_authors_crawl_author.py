# Generated by Django 5.0.6 on 2024-06-17 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawl', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crawl',
            old_name='authors',
            new_name='author',
        ),
    ]
