# Generated by Django 3.0.4 on 2020-04-22 01:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorApp', '0018_auto_20200420_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loggeduser',
            name='currentTimeStamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 21, 21, 36, 46, 376528)),
        ),
    ]
