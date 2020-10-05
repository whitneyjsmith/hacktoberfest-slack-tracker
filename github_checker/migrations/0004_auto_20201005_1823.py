# Generated by Django 3.1.2 on 2020-10-05 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github_checker', '0003_auto_20201003_0518'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationsettings',
            name='bot_avatar',
            field=models.CharField(default=':robot_face:', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notificationsettings',
            name='bot_name',
            field=models.CharField(default='Slackbot', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notificationsettings',
            name='channel',
            field=models.CharField(default='@dj', max_length=255),
            preserve_default=False,
        ),
    ]