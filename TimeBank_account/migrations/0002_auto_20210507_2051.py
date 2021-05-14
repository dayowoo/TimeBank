# Generated by Django 3.1.7 on 2021-05-07 11:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('TimeBank_app', '0001_initial'),
        ('TimeBank_account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Transfer', to='TimeBank_app.post'),
        ),
        migrations.AddField(
            model_name='account',
            name='taker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taker', to=settings.AUTH_USER_MODEL, verbose_name='받는사람'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]