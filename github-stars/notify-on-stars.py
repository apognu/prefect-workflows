import requests

from datetime import timedelta
from prefect import flow, task, variables
from prefect.blocks.system import Secret
from prefect.tasks import task_input_hash

from common import push


def fetch_stars(repo: str):
    response = requests.get(f"https://api.github.com/repos/{repo}").json()

    return response["stargazers_count"]


@task
def fetch_current_stars(repo: str):
    return fetch_stars(repo)


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(weeks=520))
def cached_stars(repo: str):
    print("Fetching actual stars for cache...")

    return fetch_stars(repo)


@flow(name="notify-on-stars")
def notify_on_stars(repo: str):
    stars = fetch_current_stars(repo)
    cached = cached_stars(repo)

    if stars > cached:
        body = f"Someone added a star on {repo} ({stars})"

        push.notify("GitHub star alert", body)
    elif cached < stars:
        body = f"Someone took back their star on {repo} ({stars})"

        push.notify("GitHub star alert", body)
