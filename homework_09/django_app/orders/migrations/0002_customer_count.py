# Generated by Django 3.2.5 on 2021-07-18 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
