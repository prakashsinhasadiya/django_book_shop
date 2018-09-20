# Generated by Django 2.0 on 2018-09-20 06:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('custom_auth', '0011_auto_20180918_0838'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordResetTokens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('token', models.CharField(max_length=60, verbose_name='Tocken ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='password_reset_token', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
