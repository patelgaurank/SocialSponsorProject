# Generated by Django 3.0.4 on 2020-09-23 13:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorApp', '0031_auto_20200507_0758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loggeduser',
            name='currentTimeStamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 23, 9, 56, 1, 977065)),
        ),
    ]
