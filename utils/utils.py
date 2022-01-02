import yaml


def convert_reiwa_to_year(reiwa: int) -> int:
    return (reiwa - 1) + 2019


def load_settings(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)
