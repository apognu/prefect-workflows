import requests

from prefect import flow, task
from prefect.blocks.system import Secret


@task(persist_result=True)
def get_name(name: str):
    return name.upper()


@task(log_prints=True)
def notify(title: str, body: str):
    username = Secret.load("pouche-webhook-username").get()
    password = Secret.load("pouche-webhook-password").get()

    requests.post(
        "https://gateway.popineau.eu/webhook/simple",
        json={"title": title, "body": body},
        auth=(username, password),
    )


@flow(name="say-hello", persist_result=True)
def say_hello(name: str, prompt: str = "Hello"):
    name = get_name(name)
    sentence = f"{prompt} {name}!"

    notify("Message from Prefect", sentence)

    return sentence
