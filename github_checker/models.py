from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
import requests
from django.conf import settings

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

    class Meta:
        unique_together = ('name', 'github_user',)

    def __str__(self):
        return self.name

    def get_pull_requests_created(self, start_date=None, end_date=None):
        base_url = "https://api.github.com/search/issues"
        qualifiers = {"author": self.github_user.username,
                      "type": "pr"}
        q_string = "+".join([f"{key}:{value}" for key, value in qualifiers.items()])
        if start_date and not end_date:
            q_string = q_string+f"+created:>={start_date.date()}"
        if end_date and not start_date:
            q_string = q_string+f"+created:<={end_date.date()}"
        if start_date and end_date:
            q_string = q_string+f"+created:{start_date.date()}..{end_date.date()}"
        auth = (settings.GITHUB_AUTH.get("username"),
                settings.GITHUB_AUTH.get("token"))
        if self.github_user.auth_token:
            auth = (self.github_user.username, self.github_user.auth_token)
        print(f"{base_url}?q={q_string}")
        print(auth)
        resp = requests.get(f"{base_url}?q={q_string}", auth=auth)
        print(resp.json())
        resp_json = resp.json()
        pr_records = []
        new_records = []
        for pr in resp_json.get("items"):
            fields = {"repo": pr.get("repository_url"),
                      "state": pr.get("state"),
                      "created_at": pr.get("created_at"),
                      "closed_at": pr.get("closed_at"),
                      "body": pr.get("body"),
                      "title": pr.get("title"),
                      "owner": self}
            pr_record, created = PullRequest.objects.get_or_create(
                                                          pull_id=pr["id"],
                                                          defaults=fields)
            pr_records.append(pr_record)
            if created:
                new_records.append(pr_record)
        return {"total_pull_requests": pr_records,
                "new_pull_requests": new_records}


class PullRequest(models.Model):
    repo = models.CharField(blank=True, max_length=255)
    pull_id = models.IntegerField(unique=True)
    state = models.CharField(blank=True, max_length=255)
    created_at = models.DateTimeField()
    closed_at = models.DateTimeField(null=True)
    body = models.CharField(blank=True, null=True, max_length=255)
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(UserConfig, on_delete=models.CASCADE, related_name="pull_requests")

    def __str__(self):
        return self.title
