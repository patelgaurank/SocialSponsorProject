# Generated by Django 3.0.4 on 2020-05-07 11:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorApp', '0030_auto_20200506_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loggeduser',
            name='currentTimeStamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 7, 7, 58, 5, 900936)),
        ),
    ]
