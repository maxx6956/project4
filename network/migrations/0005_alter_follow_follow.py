# Generated by Django 4.0.4 on 2022-06-10 22:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_alter_follow_follow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='follow',
            field=models.ManyToManyField(blank=True, null=True, related_name='Follows', to=settings.AUTH_USER_MODEL),
        ),
    ]
