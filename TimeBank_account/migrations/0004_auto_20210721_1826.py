# Generated by Django 3.1.7 on 2021-07-21 18:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TimeBank_account', '0003_user_star'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='star',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='평균평점'),
        ),
    ]
