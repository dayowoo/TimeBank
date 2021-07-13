# Generated by Django 3.1.7 on 2021-07-12 11:45

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('TimeBank_app', '0011_auto_20210628_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='댓글작성자'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='댓글등록시간')),
                ('content', models.TextField()),
                ('hour', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='실거래시간')),
                ('star', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='후기작성자')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TimeBank_app.post', verbose_name='글')),
            ],
        ),
    ]