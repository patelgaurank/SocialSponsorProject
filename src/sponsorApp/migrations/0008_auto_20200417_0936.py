# Generated by Django 3.0.4 on 2020-04-17 13:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorApp', '0007_auto_20200416_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loggeduser',
            name='currentTimeStamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 17, 9, 36, 40, 678919)),
        ),
    ]
