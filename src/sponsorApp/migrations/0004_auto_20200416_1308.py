# Generated by Django 3.0.4 on 2020-04-16 17:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorApp', '0003_auto_20200414_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loggeduser',
            name='currentTimeStamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 16, 13, 8, 46, 241888)),
        ),
    ]
