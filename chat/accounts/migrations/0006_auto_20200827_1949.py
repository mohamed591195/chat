# Generated by Django 3.1 on 2020-08-27 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200826_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='content',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='verb',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
