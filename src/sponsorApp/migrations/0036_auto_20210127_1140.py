# Generated by Django 3.1 on 2021-01-27 16:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorApp', '0035_auto_20210127_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loggeduser',
            name='currentTimeStamp',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 27, 11, 40, 12, 318678)),
        ),
    ]
