"""Configuration file loading utilities."""

import os

import yaml

from .settings import CONFIG_FILE


def load_config(config_path=None):
    """Load configuration from YAML file.

    Args:
        config_path: Optional path to config file. If None, uses default CONFIG_FILE

    Returns:
        Dictionary with configuration settings

    Raises:
        SystemExit: If configuration file is not found
    """
    if config_path is None:
        config_path = CONFIG_FILE

    if not os.path.exists(config_path):
        print(f"[ERROR] Configuration file not found: {config_path}")
        print("[INFO] Please create an input.yaml file with the required configuration")
        exit(1)

    with open(config_path, encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config
