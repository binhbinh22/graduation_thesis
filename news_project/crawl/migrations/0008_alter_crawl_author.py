# Generated by Django 5.0.6 on 2024-06-23 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawl', '0007_remove_crawl_is_collecteds_crawl_is_extract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crawl',
            name='author',
            field=models.CharField(choices=[('VNexpress', 'VNexpress'), ('Vietnam Biz', 'Vietnam Biz'), ('Cafef', 'Cafef'), ('VnEconomy', 'VnEconomy'), ('Mobiagri', 'Mobiagri'), ('Thanh niên', 'Thanh niên'), ('Tạp chí công thương', 'Tạp chí công thương')], max_length=20),
        ),
    ]
