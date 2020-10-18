import github_checker.clients.abstract_client as abstract_client
import requests
from django.conf import settings
from dateparser import parse


class Client(abstract_client.Client):
    @classmethod
    def get_pull_requests(self, user_config, **kwargs):
        base_url = "https://hacktoberfestchecker.jenko.me/prs"
        github_username = user_config.github_user.username
        resp_json = requests.get(f"{base_url}?username={github_username}").json()
        repos = []
        for pr in resp_json.get("prs", {}):
            fields = {"repo": f"https://api.github.com/repos/{pr.get('repo_name')}",
                      "url": pr.get("url"),
                      "pull_id": pr["number"],
                      "state": "closed" if pr.get("closed") else "open",
                      "created_at": parse(pr.get("created_at")),
                      "body": "",
                      "title": pr.get("title"),
                      "owner": user_config,
                      "has_hacktoberfest_label": pr.get("has_hacktoberfest_label"),
                      "repo_has_hacktoberfest_topic": pr.get("repo_has_hacktoberfest_topic")}
            repos.append(fields)
        return repos