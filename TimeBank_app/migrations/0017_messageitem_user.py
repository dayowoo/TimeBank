# Generated by Django 3.1.7 on 2021-04-06 23:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('TimeBank_app', '0016_auto_20210407_0806'),
    ]

    operations = [
        migrations.AddField(
            model_name='messageitem',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='TimeBank_account.user', verbose_name='신청자'),
            preserve_default=False,
        ),
    ]