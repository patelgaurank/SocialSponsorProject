# Generated by Django 3.2.5 on 2022-02-25 20:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorApp', '0049_auto_20210726_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loggeduser',
            name='currentTimeStamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 25, 15, 18, 57, 306157)),
        ),
    ]
