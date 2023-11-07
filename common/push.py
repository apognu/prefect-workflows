import requests

from prefect import flow, variables
from prefect.blocks.system import Secret


@flow
def notify(title: str, body: str):
    host = variables.get("pouche_host")
    username = Secret.load("pouche-webhook-username").get()
    password = Secret.load("pouche-webhook-password").get()

    requests.post(
        f"{host}/webhook/simple",
        json={
            "title": title,
            "body": body,
        },
        auth=(username, password),
    )
