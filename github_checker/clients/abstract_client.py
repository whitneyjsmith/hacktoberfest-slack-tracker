from abc import (ABCMeta, abstractmethod, )


class Client(metaclass=ABCMeta):

    @abstractmethod
    def get_pull_requests(self, user_config, **kwargs):
        repos = []
        repo_template = {"repo": "",
                         "pull_id": "",
                         "state": "",
                         "created_at": "",
                         "body": "",
                         "title": "",
                         "owner": user_config,
                         "has_hacktoberfest_label": "",
                         "repo_has_hacktoberfest_label": "",
                         "merged": ""}
        return repos
