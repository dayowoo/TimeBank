# Generated by Django 3.1.7 on 2021-09-07 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TimeBank_account', '0009_auto_20210830_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='take',
            field=models.CharField(choices=[('청소 / 심부름', '청소 / 심부름'), ('몸 가꾸기 / 치장하기', '몸 가꾸기 / 치장하기'), ('수선/ 수리', '수선/ 수리'), ('상담', '상담'), ('이동', '이동'), ('먹기', '먹기'), ('교육 / 여가생활', '교육 / 여가생활'), ('정서지지', '정서지지'), ('돌봄', '돌봄'), ('식물 가꾸기', '식물 가꾸기'), ('모임 장소 대여', '모임 장소 대여'), ('의사소통', '의사소통'), ('건강관리', '건강관리'), ('기타', '기타')], default='청소 / 심부름', max_length=50, verbose_name='받고싶어요'),
        ),
    ]
