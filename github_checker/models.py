from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
import requests
from django.conf import settings
import importlib

# Create your models here.


class GithubUserConfig(models.Model):
    username = models.CharField(max_length=255)
    id = models.IntegerField(primary_key=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    gravatar_id = models.CharField(max_length=255, blank=True, null=True)
    auth_token = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username


class NotificationSetting(models.Model):
    name = models.CharField(max_length=200, unique=True)
    start_date = models.CharField(max_length=255)
    end_date = models.CharField(max_length=255, blank=True, null=True)
    count_quota = models.IntegerField(blank=True, null=True)
    message = models.TextField()
    channel = models.CharField(max_length=255)
    bot_name = models.CharField(max_length=255)
    bot_avatar = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class SlackOrg(models.Model):
    name = models.CharField(max_length=200)
    team_id = models.CharField(max_length=20)
    bot_user_id = models.CharField(max_length=20)
    bot_access_token = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Authorized Company Slack Account'
        verbose_name_plural = 'Authorized Company Slack Accounts'


class ConnectionUserConfig(models.Model):
    slack_name = models.CharField(max_length=255)
    slack_id = models.CharField(max_length=255)
    slack_org = models.ForeignKey(SlackOrg, on_delete=models.CASCADE)
    notification_settings = models.ForeignKey(NotificationSetting, on_delete=models.CASCADE)

    def __str__(self):
        return self.slack_name


class UserConfig(models.Model):
    name = models.CharField(max_length=255, unique=True)
    watch_for_pull_requests = models.BooleanField(default=False)
    notify_count_in_slack = models.BooleanField(default=False)
    github_user = models.ForeignKey(GithubUserConfig, on_delete=models.CASCADE)
    conn_configs = models.ManyToManyField(ConnectionUserConfig)
    client = models.CharField(default="hacktoberfestchecker", max_length=255)

    class Meta:
        unique_together = ('name', 'github_user',)

    def __str__(self):
        return self.name

    def get_pull_requests_created(self, start_date=None, end_date=None):
        client = importlib.import_module(f"github_checker.clients.{self.client}")
        valid_prs = client.Client.get_pull_requests(self,
                                                    start_date=start_date,
                                                    end_date=end_date)
        pr_records = []
        new_records = []
        for pr in valid_prs:
            url = pr.pop("url")
            pr_record, created = PullRequest.objects.get_or_create(
                                                          url=url,
                                                          defaults=pr)
            pr_records.append(pr_record)
            if created:
                new_records.append(pr_record)
        return {"total_pull_requests": pr_records,
                "new_pull_requests": new_records}


class PullRequest(models.Model):
    repo = models.CharField(blank=True, max_length=255)
    url = models.CharField(max_length=255)
    pull_id = models.IntegerField()
    state = models.CharField(blank=True, max_length=255)
    created_at = models.DateTimeField()
    body = models.CharField(blank=True, null=True, max_length=255)
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(UserConfig, on_delete=models.CASCADE, related_name="pull_requests")
    has_hacktoberfest_label = models.BooleanField(default=False)
    repo_has_hacktoberfest_topic = models.BooleanField(default=False)
    merged = models.BooleanField(default=False)
    alerted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
