# Generated by Django 3.1.7 on 2021-06-22 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TimeBank_app', '0006_auto_20210622_1325'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='post',
        ),
    ]