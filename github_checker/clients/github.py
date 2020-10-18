import github_checker.clients.abstract_client as abstract_client
import requests
from django.conf import settings
from pprint import pprint


class Client(abstract_client.Client):
    @classmethod
    def get_pull_requests(self, user_config, **kwargs):
        repos = []
        start_date = kwargs.get("start_date")
        end_date = kwargs.get("end_date")
        base_url = "https://api.github.com/search/issues"
        qualifiers = {"author": user_config.github_user.username,
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
        if user_config.github_user.auth_token:
            auth = (user_config.github_user.username,
                    user_config.github_user.auth_token)
        print(f"{base_url}?q={q_string}")
        print(auth)
        resp = requests.get(f"{base_url}?q={q_string}", auth=auth)
        print(resp.json())
        resp_json = resp.json()
        headers = {"Accept": "application/vnd.github.mercy-preview+json"}
        for pr in resp_json.get("items"):
            details = requests.get(pr.get("pull_request", {}).get("url"),
                                   auth=auth).json()
            repo_topics = []
            if pr.get("repository_url"):
                repo_topics = requests.get(
                    f'{pr.get("repository_url")}/topics',
                    headers=headers, auth=auth).json()
            fields = {"repo": pr.get("repository_url"),
                      "url": pr.get("html_url"),
                      "pull_id": pr["id"],
                      "state": pr.get("state"),
                      "created_at": pr.get("created_at"),
                      "body": pr.get("body"),
                      "title": pr.get("title"),
                      "owner": user_config,
                      "has_hacktoberfest_label": "hacktoberfest-accepted"
                      in pr.get("labels", []),
                      "repo_has_hacktoberfest_topic": "hactoberfest"
                      in repo_topics,
                      "merged": details.get("merged", False)}

            # Only count ones that match the new Hacktoberfest Rules
            if ((fields["has_hacktoberfest_label"] or
                    fields["repo_has_hacktoberfest_topic"]) or
                    fields["merged"]):
                repos.append(fields)
        return repos
