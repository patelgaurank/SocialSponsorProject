# Generated by Django 3.0.4 on 2020-04-15 00:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loggeduser',
            name='currentTimeStamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 14, 20, 8, 36, 269377)),
        ),
    ]