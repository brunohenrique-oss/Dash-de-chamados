import requests
import json
import os
from requests.auth import HTTPBasicAuth

url = os.environ["JIRA_BASE_URL"]
email = os.environ["JIRA_EMAIL"]
token = os.environ["JIRA_API_TOKEN"]

jql = 'project = STI AND "Tipo de solicitação" = "Correção Causa Raiz (STI)" AND statusCategory != Done ORDER BY created DESC'

api_url = f"{url}/rest/api/3/search"

headers = {
    "Accept": "application/json"
}

params = {
    "jql": jql,
    "maxResults": 100
}

response = requests.get(
    api_url,
    headers=headers,
    params=params,
    auth=HTTPBasicAuth(email, token)
)

response.raise_for_status()
data = response.json()

issues = []

for issue in data.get("issues", []):
    fields = issue["fields"]

    issues.append({
        "key": issue["key"],
        "summary": fields.get("summary"),
        "status": fields.get("status", {}).get("name"),
        "created": fields.get("created"),
        "priority": fields.get("priority", {}).get("name") if fields.get("priority") else None,
        "assignee": fields.get("assignee", {}).get("displayName") if fields.get("assignee") else None,
        "url": f"{url}/browse/{issue['key']}"
    })

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(issues, f, ensure_ascii=False, indent=2)

print(f"{len(issues)} chamados exportados para data.json")
