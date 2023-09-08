import os
import json
import requests

# GitHub Personal Access Token für Authentifizierung
access_token = os.environ.get('SECOND')

# Lese die Konfigurationsdatei ein
with open("project/settings.json", "r") as config_file:
    config = json.load(config_file)

# GitHub API-Endpunkt für Repository-Einstellungen
api_url = "https://api.github.com/users/Dalghazal/repos"

# Funktion zum Aktualisieren der Repository-Einstellungen
def update_repository_settings(repo_config):
    repo_name = repo_config["name"]
    branch_protection = {
        "required_status_checks": None,
        "enforce_admins": None,
        "required_pull_request_reviews": {
            "required_approving_review_count": repo_config["required_approvals"],
            "dismiss_stale_reviews": False
        },
        "restrictions": {
            "users": repo_config["collaborators"]
        }
    }
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.luke-cage-preview+json"
    }

    response = requests.put(f"{api_url}/{repo_name}/branches/main/protection", headers=headers, json=branch_protection)
    if response.status_code == 200:
        print(f"Repository {repo_name} aktualisiert.")
    else:
        print(f"Fehler beim Aktualisieren von Repository {repo_name}.")

# Durchlaufe die Liste der Repository-Konfigurationen und aktualisiere die Einstellungen
for repo_config in config["repositories"]:
    update_repository_settings(repo_config)



