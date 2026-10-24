from mitmproxy import http
import json
import os

authfilething = os.path.join(os.path.dirname(os.path.abspath(__file__)), "auth.txt")


def getResponse():
    with open(authfilething, "r", encoding="utf-8") as file:
        content = file.read()

    return json.loads(content)


def request(flow: http.HTTPFlow):
    if (flow.request.method == "POST" and flow.request.pretty_host == "auth.epicquest.app" and flow.request.path.split("?")[0] == "/connect/token"):
        flow.metadata["override_token_response"] = True


def response(flow: http.HTTPFlow):
    if not flow.metadata.get("override_token_response"):
        return

    try:
        token_response = getResponse()
    except (OSError, json.JSONDecodeError) as error:
        print(f"uh oh: {error}")
        return

    flow.response.status_code = 200
    flow.response.headers["Content-Type"] = "application/json"
    flow.response.headers.pop("Content-Encoding", None)
    flow.response.headers.pop("Transfer-Encoding", None)
    flow.response.text = json.dumps(token_response)
