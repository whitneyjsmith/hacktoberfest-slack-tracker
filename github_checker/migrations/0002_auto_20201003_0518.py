# Generated by Django 3.1.2 on 2020-10-03 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('github_checker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectionUserConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('slack_id', models.CharField(max_length=255)),
            ],
        ),
        migrations.RenameField(
            model_name='notificationsettings',
            old_name='range_to_look_at',
            new_name='start_date',
        ),
        migrations.RemoveField(
            model_name='userconfig',
            name='slack_user',
        ),
        migrations.AddField(
            model_name='notificationsettings',
            name='end_date',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pullrequest',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pull_requests', to='github_checker.userconfig'),
        ),
        migrations.DeleteModel(
            name='SlackUserConfig',
        ),
        migrations.AddField(
            model_name='connectionuserconfig',
            name='notification_settings',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='github_checker.notificationsettings'),
        ),
        migrations.AddField(
            model_name='connectionuserconfig',
            name='slack_org',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='github_checker.slackorg'),
        ),
        migrations.AddField(
            model_name='userconfig',
            name='conn_configs',
            field=models.ManyToManyField(null=True, to='github_checker.ConnectionUserConfig'),
        ),
    ]