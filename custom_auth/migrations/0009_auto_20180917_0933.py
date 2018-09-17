# Generated by Django 2.0 on 2018-09-17 09:33

from django.db import migrations
import slugger.fields


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0008_auto_20180917_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookdetail',
            name='slug',
            field=slugger.fields.AutoSlugField(blank=True, null=True, populate_from='book_name', unique=True),
        ),
    ]
