# Generated by Django 3.1.7 on 2021-05-24 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TimeBank_account', '0004_auto_20210524_1734'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='balance',
        ),
        migrations.AddField(
            model_name='account',
            name='giver_balance',
            field=models.IntegerField(default=0, verbose_name='주는사람 잔액'),
        ),
        migrations.AddField(
            model_name='account',
            name='taker_balance',
            field=models.IntegerField(default=0, verbose_name='받는사람 잔액'),
        ),
    ]
