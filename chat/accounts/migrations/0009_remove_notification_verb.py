# Generated by Django 3.1 on 2020-08-30 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20200830_1343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='verb',
        ),
    ]
