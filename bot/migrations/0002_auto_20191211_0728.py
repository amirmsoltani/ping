# Generated by Django 2.2.3 on 2019-12-11 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='game',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='gender',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='tourism',
            field=models.IntegerField(null=True),
        ),
    ]
