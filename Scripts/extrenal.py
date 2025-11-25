import requests

token = "SEU_TOKEN"

url = f"https://api.github.com/repos/PedroZulim/ponto-automatico/actions/workflows/ponto.yml/dispatches"

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

data = {"ref": "main"}

r = requests.post(url, headers=headers, json=data)
