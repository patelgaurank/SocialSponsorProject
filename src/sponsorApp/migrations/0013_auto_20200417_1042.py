# Generated by Django 3.0.4 on 2020-04-17 14:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorApp', '0012_auto_20200417_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loggeduser',
            name='currentTimeStamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 17, 10, 42, 34, 475375)),
        ),
    ]
