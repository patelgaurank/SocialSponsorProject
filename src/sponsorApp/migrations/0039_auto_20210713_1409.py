# Generated by Django 3.1 on 2021-07-13 18:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorApp', '0038_auto_20210713_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loggeduser',
            name='currentTimeStamp',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 13, 14, 9, 4, 152346)),
        ),
    ]
