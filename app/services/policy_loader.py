import yaml
from pathlib import Path

POLICE_FILE = Path("policies/access_policies.yaml")

def load_policies():
    if not POLICE_FILE.exists():
        return []

    with open(POLICE_FILE, "r") as file:
        return yaml.safe_load(file)
    
def save_policies(policies: list):
    with open(POLICE_FILE, "w") as file:
        yaml.safe_dump(policies, file, default_flow_style=False, sort_keys=False, allow_unicode=True)