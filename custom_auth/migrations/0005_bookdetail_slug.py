# Generated by Django 2.0 on 2018-09-12 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0004_auto_20180911_0559'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookdetail',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True),
        ),
    ]
