# Generated by Django 3.1.7 on 2021-03-19 05:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TimeBank_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='main_work',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TimeBank_app.maincategory'),
        ),
        migrations.AlterField(
            model_name='post',
            name='sub_work',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='MainCategory', to='TimeBank_app.subcategory'),
        ),
    ]