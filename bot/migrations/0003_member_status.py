# Generated by Django 2.2.3 on 2019-12-11 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_auto_20191211_0728'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
