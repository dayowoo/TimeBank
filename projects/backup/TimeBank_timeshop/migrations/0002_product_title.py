# Generated by Django 3.1.7 on 2021-09-13 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TimeBank_timeshop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='title',
            field=models.CharField(default='example', max_length=200, verbose_name='제목'),
        ),
    ]
