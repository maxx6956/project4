# Generated by Django 4.0.4 on 2022-06-12 05:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_follow_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='following',
        ),
    ]
