# Generated by Django 2.0 on 2020-02-27 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxapp', '0006_auto_20200222_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersmessagemysqldb',
            name='case1',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='usersmessagemysqldb',
            name='case2',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='usersmessagemysqldb',
            name='case3',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='usersmessagemysqldb',
            name='case4',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
