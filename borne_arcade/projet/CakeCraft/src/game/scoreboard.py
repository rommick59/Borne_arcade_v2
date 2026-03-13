import json
import os

_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
)
_PATH = os.path.join(_DIR, "scoreboard.json")
_ARCADE_PATH = os.path.join(
    _DIR, "highscore"
)  # format NOM-SCORE compatible with arcade Java reader

_TOP = 10


def _load() -> dict:
    if not os.path.exists(_PATH):
        return {"solo": [], "vs": []}
    try:
        with open(_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "solo" not in data:
            data["solo"] = []
        if "vs" not in data:
            data["vs"] = []
        return data
    except Exception:
        return {"solo": [], "vs": []}


def _save(data: dict):
    with open(_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    _sync_arcade(data)


def _sync_arcade(data: dict):
    """Write highscore.txt in NOM-SCORE format readable by the arcade Java code."""
    entries = sorted(data["solo"], key=lambda e: e["score"], reverse=True)[:_TOP]
    with open(_ARCADE_PATH, "w", encoding="utf-8") as f:
        for i, e in enumerate(entries):
            f.write(f"{e['name']}-{e['score']}")
            if i != len(entries) - 1:
                f.write("\n")


def add_solo(name: str, score: int):
    """Save a solo (player vs bot) score entry."""
    data = _load()
    data["solo"].append({"name": name, "score": score})
    data["solo"].sort(key=lambda e: e["score"], reverse=True)
    data["solo"] = data["solo"][:_TOP]
    _save(data)


def add_vs(name1: str, score1: int, name2: str, score2: int):
    """Save a 1v1 entry — kept as chronological history, last 20 games."""
    data = _load()
    data["vs"].append(
        {
            "name1": name1,
            "score1": score1,
            "name2": name2,
            "score2": score2,
            "total": score1 + score2,
        }
    )
    data["vs"] = data["vs"][-20:]  # keep only the 20 most recent
    _save(data)


def get_solo() -> list:
    return _load()["solo"]


def get_vs() -> list:
    return _load()["vs"]
