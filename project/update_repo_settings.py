import os
import json
import subprocess

# Lese die Konfigurationsdatei ein
with open("settings.json", "r") as config_file:
    config = json.load(config_file)

# GitHub CLI-Befehl für das Aktualisieren von Repository-Einstellungen
gh_command = "gh repo set"

# Durchlaufe die Liste der Repository-Konfigurationen und aktualisiere die Einstellungen
for repo_config in config["repositories"]:
    repo_name = repo_config["name"]
    collaborators = ",".join(repo_config["collaborators"])
    branch_protection = json.dumps(repo_config["branch_protection"])
    
    # Konstruiere den GitHub CLI-Befehl
    command = f"{gh_command} {repo_name} -b '{branch_protection}' --required-approvals {repo_config['required_approvals']} --squash-merge {repo_config['squash_merge']} --collaborators {collaborators}"

    # Führe den Befehl aus
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print(f"Repository {repo_name} aktualisiert.")
    else:
        print(f"Fehler beim Aktualisieren von Repository {repo_name}:")
        print(result.stderr)
