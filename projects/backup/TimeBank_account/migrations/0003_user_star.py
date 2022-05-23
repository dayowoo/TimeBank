# Generated by Django 3.1.7 on 2021-07-21 11:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TimeBank_account', '0002_account_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='star',
            field=models.IntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
            preserve_default=False,
        ),
    ]