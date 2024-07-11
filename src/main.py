import requests
# import json
from utils import create_jwt

from typing import Literal

# 上の階層のディレクトリをimportするための設定
import sys
sys.path.append('../')  # noqa
from customTypes import GithubIssue, GithubIssuesComment

# .envを読み込む
import dotenv
dotenv.load_dotenv()


class GitHubApp:
    def __init__(self, owner: str, repo: str):
        self.owner = owner
        self.repo = repo

        self.token = ''

    def _set_header():
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                if not self.token:
                    self.token = self.cretate_token()
                self.headers = {
                    "Accept": "application/vnd.github+json",
                    "Authorization": f"Bearer {self.token}",
                    "X-GitHub-Api-Version": "2022-11-28"
                }
                return func(self, *args, **kwargs)
            return wrapper
        return decorator

    def cretate_token(self):
        jwt = create_jwt()
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {jwt}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        response = requests.post(
            "https://api.github.com/app/installations/52660613/access_tokens",
            headers=self.headers
        )
        return response.json()['token']

    @_set_header()
    def get_issues(self, page=1, per_page=100) -> list[GithubIssue]:
        url = f'https://api.github.com/repos/{self.owner}/{self.repo}/issues?page={page}&per_page={per_page}'
        response = requests.get(url, headers=self.headers)

        link_str = response.headers.get('Link', '')

        next_pages = link_str.split(', ')
        is_has_next = False
        for next_page in next_pages:
            if 'rel="next"' in next_page:
                is_has_next = True
                link_str = next_page
                break
        if link_str and is_has_next:
            next_page_int: int = int(link_str.split('page=')[1].split('&')[0])

            val = [
                GithubIssue(**issue) for issue in response.json()
            ] + self.get_issues(next_page_int, per_page)
            return sorted(val, key=lambda x: x.id, reverse=True)

        return [GithubIssue(**issue) for issue in response.json()]

    @_set_header()
    def get_issue(self, number: int, state: Literal['open', 'closed', 'all'] = 'open'):
        url = f'https://api.github.com/repos/{self.owner}/{self.repo}/issues/{number}?state={state}'
        response = requests.get(url, headers=self.headers)

        res = self._get_issue_comment(number)

        dict_data = response.json()
        dict_data['comments'] = res

        return GithubIssue(**dict_data)

    def _get_issue_comment(self, number: int) -> list[GithubIssuesComment]:
        url = f'https://api.github.com/repos/{self.owner}/{self.repo}/issues/{number}/comments'
        response = requests.get(url, headers=self.headers)
        return [GithubIssuesComment(**comment) for comment in response.json()]

    @_set_header()
    def send_comment(self, number: int, body: str):
        url = f'https://api.github.com/repos/{self.owner}/{self.repo}/issues/{number}/comments'
        response = requests.post(url, headers=self.headers, json={"body": body})
        return response.json()
