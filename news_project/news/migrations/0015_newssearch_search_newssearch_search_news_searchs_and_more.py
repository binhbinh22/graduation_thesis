# Generated by Django 5.0.6 on 2024-06-04 05:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0014_save_news_save_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsSearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.news')),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('newss', models.ManyToManyField(through='news.NewsSearch', to='news.news')),
            ],
        ),
        migrations.AddField(
            model_name='newssearch',
            name='search',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.search'),
        ),
        migrations.AddField(
            model_name='news',
            name='searchs',
            field=models.ManyToManyField(through='news.NewsSearch', to='news.search'),
        ),
        migrations.AlterUniqueTogether(
            name='newssearch',
            unique_together={('news', 'search')},
        ),
    ]
