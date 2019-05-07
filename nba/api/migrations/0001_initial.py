# Generated by Django 2.2.1 on 2019-05-06 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('url', models.URLField()),
                ('published_time', models.DateTimeField()),
                ('news_source', models.CharField(max_length=30)),
                ('news_reporter', models.CharField(max_length=30)),
                ('news_type', models.CharField(max_length=30)),
                ('news_content', models.TextField()),
            ],
        ),
    ]
