import installDependencies

import requests # type: ignore
import getpass
import json

modifyKey = True
valueToPutInKey = "aGVsbG8gcmFuZG9tIHBlcnNvbiwgZ2FiZSBuZXJmZWQgdGhlIHdlYiBhdXRoIHNvIEkgcHV0IHNvbWUgZ2FyYmFnZSBpbiBoZXJlIHRvIG1ha2UgaXQgd29yayBhZ2Fpbg=="

url = "https://auth.epicquest.app/connect/token/web"


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

def authenticate(username, password):
    success = False
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
            newBodyJson = response.json()
            if modifyKey == True:
                newBodyJson["key"] = valueToPutInKey
                body = json.dumps(newBodyJson, indent=4)
            if response.json().get("error") is not None:
                print(f"Error: {response.json().get('error')}")
                print(body)
            else:
                success = True
                print("Authentication successful")
        except ValueError:
            body = response.text

        with open("auth.txt", "w", encoding="utf-8") as file:
            file.write(body)

        print("authentication written to auth.txt")

        return {"success": success, "error_description": response.json().get("error_description")}

    except requests.RequestException as error:
        print("fail:", error)

if __name__ == "__main__":
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    authenticate(username, password)
    print("run EpicQuest then startAuthProxy.sh or .bat")
    print("On Linux it is important to run the sh script after the game reaches the login screen or else it won't be able to connect")
    print("You may need to press F1 in game to reload the login screen after running script (reloadLoginScreen.dll should be installed)")

