import installDependencies

import requests
import getpass
import json

url = "https://auth.epicquest.app/connect/token/web"

username = input("Username: ")
password = getpass.getpass("Password: ")

headers = {
    "Origin": "https://epicquest.app",
    "Referer": "https://epicquest.app/",
    "Accept": "*/*",
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/60.5 Safari/605.1.15"
    )
}

data = {
    "username": username,
    "password": password
}

try:
    response = requests.post(
        url,
        headers=headers,
        files={
            "username": (None, username),
            "password": (None, password)
        },
        timeout=30
    )

    try:
        body = json.dumps(response.json(), indent=4)
    except ValueError:
        body = response.text

    with open("auth.txt", "w", encoding="utf-8") as file:
        print(f"status: {response.status_code}")
        file.write(body)

    print("authentication written to auth.txt, run EpicQuest then startAuthProxy.sh or .bat")
    print("On Linux it is important to run the sh script after the game reaches the login screen or else it won't be able to connect")
    print("You may need to press F1 in game to reload the login screen after running script (reloadLoginScreen.dll should be installed)")

except requests.RequestException as error:
    print("fail:", error)
