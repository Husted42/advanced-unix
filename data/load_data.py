import requests

def download_file(url, output_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)

download_file("https://teaching.healthtech.dtu.dk/material/22118/people.db", "people.db")