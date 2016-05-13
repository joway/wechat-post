from github3 import login

from config import local_settings

github = login(local_settings.github_username, password=local_settings.github_password)
username = local_settings.github_username
repo = 'wechat-issues'
num = 1
issue = github.issue(username, repo, num)


def comment_on_github(text):
    issue.create_comment(text)
    print(text)
