from .models import UserConfig
import dateutil.parser as parser
from datetime import datetime
import requests
import os
from django.conf import settings


def get_user_github(github_username):
    auth = (settings.GITHUB_AUTH.get("username"),
            settings.GITHUB_AUTH.get("token"))
    url = f"https://api.github.com/users/{github_username}"
    resp = requests.get(url, auth=auth).json()
    if "login" not in resp:
        return False
    return {"username": resp.get("login"),
            "id": resp.get("id"),
            "gravatar_id": resp.get("gravatar_id"),
            "avatar": resp.get("avatar_url"),
            "name": resp.get("name") or resp.get("login")}


def check_user_and_update(user):
    user_notifs = user.conn_configs.all()
    print("user notifs!")
    print(user_notifs)
    for notif in user_notifs:
        print(notif)
        notif_settings = notif.notification_settings
        start_date_str = notif_settings.start_date
        end_date_str = notif_settings.end_date
        start_date = parser.parse(start_date_str)
        end_date = parser.parse(end_date_str) if end_date_str else datetime.now()
        if start_date_str.count(" ") == 1:  # If we only have month and year. TODO make this more robust
            start_date = start_date.replace(day=1)
        print("Start Date!")
        print(start_date)
        prs = user.get_pull_requests_created(start_date=start_date, end_date=end_date)
        if prs.get("new_pull_requests"):
            variables = {"github_user": user.github_user,
                         "user": user,
                         "self": notif_settings,
                         "slack_user": notif,
                         "num_new_requests": len(prs.get("total_pull_requests"))}
            message = notif_settings.message.format(**variables)
            token = notif.slack_org.bot_access_token
            channel = notif_settings.channel
            bot_name = notif_settings.bot_name
            bot_avatar = notif_settings.bot_avatar
            post_message_to_slack(token, message, channel,
                                  bot_name, bot_avatar)


def post_message_to_slack(token, message, channel_id, username, icon):
    params = {"token": token,
              "channel": channel_id,
              "text": message,
              "as_user": False,
              "username": username}
    if icon and icon[0] == ":":
        params["icon_emoji"] = icon
    elif icon:
        params["icon_url"] = icon
    requests.post("https://slack.com/api/chat.postMessage",
                  params=params)

    return True


def run_check_and_update():
    users = list(UserConfig.objects.filter(watch_for_pull_requests=True).all())
    # TODO: update this to use multiprocessing pools rather than looping
    for user in users:
        check_user_and_update(user)
