import os
import sys
import subprocess
import unicodedata
from pathlib import Path


try:
    import yaml
except ImportError:
    print("Error: pyyaml not installed. Run: pip3 install pyyaml", file=sys.stderr)
    sys.exit(1)

CONFIG_PATH = Path(__file__).parent / "config.yaml"

ANSI = {
    "bold":   "\033[1m",
    "cyan":   "\033[36m",
    "gray":   "\033[90m",
    "yellow": "\033[33m",
    "reset":  "\033[0m",
}

def colored(text: str, color: str) -> str:
    return f"{ANSI[color]}{text}{ANSI['reset']}"

def print_header(label: str, usage: str):
    print()
    print(colored(f"{label} : {usage}", "cyan"))
    print(colored("──────────────────────────────────", "cyan"))

def _ljust_display(s: str, width: int) -> str:
    dw = sum(2 if unicodedata.east_asian_width(c) in ("W", "F") else 1 for c in s)
    return s + " " * max(0, width - dw)

def print_item(i: int, name: str, usage: str):
    print(f"{colored(f'{i}. {_ljust_display(name, 13)}', 'bold')}: {usage}")

def print_subitem(i: int, j: int, name: str, usage: str, description: str):
    print(colored(f"   {i}-{j}. {_ljust_display(name, 20)}: {_ljust_display(usage, 6)}  {description}", "gray"))

def get_dir_usage(path: Path) -> str:
    if not path.is_dir():
        return "없음"
    r = subprocess.run(["du", "-sh", str(path)], capture_output=True, text=True)
    return r.stdout.split()[0] if r.returncode == 0 else "없음"

def get_dirs_usage(paths: list[Path]) -> str:
    existing = [str(p) for p in paths if p.is_dir()]
    if not existing:
        return "없음"
    r = subprocess.run(["du", "-shc"] + existing, capture_output=True, text=True)
    if r.returncode == 0:
        return r.stdout.strip().splitlines()[-1].split()[0]
    return "없음"

def load_config() -> list:
    with open(CONFIG_PATH) as f:
        config = yaml.safe_load(f)
    categories = []
    for cat in config["categories"]:
        apps = []
        for item in cat["apps"]:
            dirs = [
                {
                    "name": d.get("name"),
                    "dir": Path(os.path.expanduser(d["dir"])),
                    "description": d.get("description", ""),
                }
                for d in item["dirs"]
            ]
            apps.append({"name": item["name"], "dirs": dirs})
        categories.append({"name": cat["name"], "apps": apps})
    return categories

def confirm(msg: str) -> bool:
    answer = input(f"\n{msg} [Y/n]: ").strip().lower()
    return answer == "y"

def print_progress(current: int, total: int):
    width = 20
    filled = int(width * current / total)
    bar = "█" * filled + "░" * (width - filled)
    print(f"\r삭제중... [{bar}] {current}/{total}", end="", flush=True)

def delete_dirs(dirs: list[Path]):
    import shutil
    total = len(dirs)
    for i, d in enumerate(dirs, 1):
        print_progress(i, total)
        if not d.is_dir():
            continue
        for child in d.iterdir():
            if child.is_dir():
                shutil.rmtree(child, ignore_errors=True)
            else:
                child.unlink(missing_ok=True)
    print()
