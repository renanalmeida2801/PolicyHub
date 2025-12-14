import yaml
from pathlib import Path

def load_policies():
    policy_path = Path("policies/access_policies.yaml")

    with open(policy_path, "r") as file:
        return yaml.safe_load(file)