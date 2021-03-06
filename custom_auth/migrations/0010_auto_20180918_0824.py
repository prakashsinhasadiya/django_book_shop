# Generated by Django 2.0 on 2018-09-18 08:24

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0009_auto_20180917_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookdetail',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, editable=False, null=True, populate_from='book_name', unique=True),
        ),
    ]
