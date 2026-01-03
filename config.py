"""
Simple JSON-backed configuration for the expense tracker.
Persists UI preferences like timestamp display mode and custom format.
"""
import json
import os
from typing import Dict

CONFIG_PATH = "config.json"

DEFAULT_CONFIG: Dict[str, object] = {
    'timestamp_mode': 'local',  # 'local', 'utc', or 'custom'
    'custom_format': '%Y-%m-%d %H:%M:%S %Z',
    'show_relative': True,
    'timezone': 'system'  # 'system' or IANA timezone name
}


def load_config(path: str = CONFIG_PATH) -> Dict[str, object]:
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    return DEFAULT_CONFIG.copy()
                # Merge with defaults to ensure keys
                cfg = DEFAULT_CONFIG.copy()
                cfg.update(data)
                return cfg
        except Exception:
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, object], path: str = CONFIG_PATH) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
