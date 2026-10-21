#!/usr/bin/env python3
"""Base de dados de worldbuilding do MUD Valinor.

Fonte da verdade: os YAML em db/data/*.yaml. O sqlite e os exports sao
gerados por este script e nunca devem ser editados a mao.

Uso:
  build.py validate      valida ids, refs e enums de todos os YAML
  build.py sqlite        gera db/valinor.sqlite a partir dos YAML
  build.py export-json   gera db/valinor.json (export portavel)
  build.py pending       lista cabecalhos '## ' do notas.md ainda nao marcados em _ingested.yaml

rooms.yaml e texts.yaml sao gerados por db/tools/minerar.py (rode ele antes do validate).
"""
from __future__ import annotations

import sys, json, sqlite3
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    sys.exit("Falta PyYAML. Instale com: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent          # db/
DATA = ROOT / "data"
DB_PATH = ROOT / "valinor.sqlite"
JSON_PATH = ROOT / "valinor.json"
NOTAS_PATH = ROOT.parent / "notas.md"

TYPES = {
    "region":   {"file": "regions.yaml",   "required": ["id", "name", "kind"],              "sources_required": True},
    "location": {"file": "locations.yaml", "required": ["id", "name", "region"],             "sources_required": False},
    "exit":     {"file": "exits.yaml",     "required": ["id", "from", "dir"],                "sources_required": False},
    "route":    {"file": "routes.yaml",    "required": ["id", "from", "to", "steps"],         "sources_required": True},
    "npc":      {"file": "npcs.yaml",      "required": ["id", "name", "roles"],               "sources_required": True},
    "item":     {"file": "items.yaml",     "required": ["id", "name", "category"],            "sources_required": True},
    "trade":    {"file": "trades.yaml",    "required": ["id", "npc", "item", "mode"],          "sources_required": False},
    "creature": {"file": "creatures.yaml", "required": ["id", "name"],                         "sources_required": True},
    "mechanic": {"file": "mechanics.yaml", "required": ["id", "name", "category"],             "sources_required": True},
    "lore":     {"file": "lore.yaml",      "required": ["id", "canon_name", "work"],           "sources_required": True},
    "event":    {"file": "events.yaml",    "required": ["id", "type", "summary"],              "sources_required": True},
    "question": {"file": "questions.yaml","required": ["id", "question", "kind", "status"],   "sources_required": True},
    # camada bruta, GERADA por db/tools/minerar.py a partir de logs/ (nao editar a mao)
    "room":     {"file": "rooms.yaml",     "required": ["id", "title", "region", "description"], "sources_required": True},
    "text":     {"file": "texts.yaml",     "required": ["id", "kind", "title", "body"],         "sources_required": True},
    "object":   {"file": "objects.yaml",   "required": ["id", "name", "kind"],                  "sources_required": True},
}

# campo -> um unico id referenciado (ou None)
REF_FIELDS = {
    "region": ["parent"],
    "location": ["region"],
    "exit": ["from", "to"],
    "route": ["from", "to", "given_by"],
    "npc": ["canon"],
    "trade": ["npc", "item"],
    "room": ["region", "location"],
    "object": ["item"],
}
# campo -> lista de ids referenciados
REF_LIST_FIELDS = {
    "region": ["tolkien_refs"],
    "exit": ["destinations"],
    "creature": ["regions", "drops"],
    "mechanic": ["instances"],
    "lore": ["mud_entities"],
    "event": ["refs"],
    "question": ["refs"],
    "text": ["rooms"],
    "object": ["rooms"],
}

ENUMS = {
    "region.kind": {"city", "hub", "road", "wilderness", "dungeon", "quest-area", "district", "building"},
    "region.safety": {"safe", "guarded", "hostile", "unknown"},
    "region.navigation": {"grid", "linear", "maze", "one-way", "wilderness", "unknown"},
    "location.kind": {"room", "segment", "building", "maze-cluster"},
    "location.status": {"explored", "partial", "seen-only", "locked", "rumored"},
    "location.light": {"lit", "dark-at-night", "needs-light"},
    "exit.selection": {"fixed", "return-to-entry", "contextual", "unknown"},
    "route.mode": {"walk", "cart", "teleport"},
    "trade.mode": {"sells", "buys", "refuses", "accepts-unpaid", "repairs"},
    "mechanic.category": {"survival", "combat", "economy", "travel", "navigation", "social", "progression", "death", "time", "parser", "meta-system"},
    "lore.fidelity": {"exact", "renamed", "adapted", "invented-in-style"},
    "event.type": {"milestone", "death", "discovery", "correction", "bug", "buff-expired"},
    "question.kind": {"trigger-unknown", "unexplored", "locked", "contradiction", "mechanic-unclear"},
    "question.status": {"open", "resolved", "abandoned"},
    "object.kind": {"item", "scenery"},
    "text.kind": {"creation", "help", "look", "shop-list", "speech", "tip", "remains"},
    "*.confidence": {"confirmed", "inferred", "hypothesis", "superseded"},
}


def load_all() -> dict[str, list[dict[str, Any]]]:
    data: dict[str, list[dict[str, Any]]] = {}
    for kind, spec in TYPES.items():
        path = DATA / spec["file"]
        items = yaml.safe_load(path.read_text()) if path.exists() else []
        data[kind] = items or []
    return data


def all_ids(data: dict[str, list[dict[str, Any]]]) -> dict[str, str]:
    ids: dict[str, str] = {}
    for kind, items in data.items():
        for it in items:
            if "id" in it:
                ids[it["id"]] = kind
    return ids


def check_ref(val: str | None, ids: dict[str, str], errors: list[str], where: str) -> None:
    if val is None:
        return
    if val not in ids:
        errors.append(f"{where}: referencia quebrada -> {val}")


def validate(data: dict[str, list[dict[str, Any]]]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    ids = all_ids(data)
    seen = set()
    for kind, items in data.items():
        spec = TYPES[kind]
        for i, it in enumerate(items):
            where = f"{kind}[{i}] ({it.get('id', '<sem id>')})"
            for field in spec["required"]:
                if field not in it or it[field] in (None, "", []):
                    errors.append(f"{where}: campo obrigatorio ausente '{field}'")
            _id = it.get("id")
            if _id:
                if _id in seen:
                    errors.append(f"{where}: id duplicado '{_id}'")
                seen.add(_id)
            if spec["sources_required"] and not it.get("sources"):
                errors.append(f"{where}: falta 'sources'")
            conf = it.get("confidence")
            if conf and conf not in ENUMS["*.confidence"]:
                errors.append(f"{where}.confidence: valor invalido '{conf}'")
            for field in REF_FIELDS.get(kind, []):
                check_ref(it.get(field), ids, errors, f"{where}.{field}")
            for field in REF_LIST_FIELDS.get(kind, []):
                for v in (it.get(field) or []):
                    check_ref(v, ids, errors, f"{where}.{field}")
            for ekey, allowed in ENUMS.items():
                etype, efield = ekey.split(".")
                if etype not in (kind, "*"):
                    continue
                val = it.get(efield)
                if val and val not in allowed:
                    errors.append(f"{where}.{efield}: valor fora do enum '{val}'")
    return errors, warnings


def cmd_validate() -> None:
    data = load_all()
    errors, warnings = validate(data)
    total = sum(len(v) for v in data.values())
    print(f"{total} entidades carregadas de {len(data)} tipos.")
    for kind, items in data.items():
        print(f"  {kind}: {len(items)}")
    for w in warnings:
        print("AVISO:", w)
    for e in errors:
        print("ERRO:", e)
    if errors:
        print(f"\n{len(errors)} erro(s). Corrija antes de gerar o sqlite.")
        sys.exit(1)
    print("\nOK — nenhum erro.")


def cmd_sqlite() -> None:
    data = load_all()
    errors, _ = validate(data)
    if errors:
        print("Existem erros de validacao — rode 'validate' primeiro.")
        sys.exit(1)
    if DB_PATH.exists():
        DB_PATH.unlink()
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    for kind, items in data.items():
        if not items:
            continue
        cols = sorted({k for it in items for k in it.keys()})
        cur.execute(f'CREATE TABLE {kind} (' + ",".join(f'"{c}" TEXT' for c in cols) + ")")
        for it in items:
            vals = []
            for c in cols:
                v = it.get(c)
                vals.append(json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v)
            cur.execute(f"INSERT INTO {kind} VALUES (" + ",".join("?" * len(cols)) + ")", vals)
    con.commit()
    con.close()
    print(f"Gerado {DB_PATH} com {sum(1 for v in data.values() if v)} tabelas.")


def cmd_export_json() -> None:
    data = load_all()
    JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"Gerado {JSON_PATH}")


def cmd_pending() -> None:
    ingested_path = DATA / "_ingested.yaml"
    ingested = set(yaml.safe_load(ingested_path.read_text()) or []) if ingested_path.exists() else set()
    headers = [l[3:].strip() for l in NOTAS_PATH.read_text().splitlines() if l.startswith("## ")]
    pending = [h for h in headers if h not in ingested]
    print(f"{len(headers)} cabecalhos em notas.md, {len(ingested)} ja ingeridos, {len(pending)} pendentes:")
    for h in pending:
        print(" -", h)


COMMANDS = {
    "validate": cmd_validate,
    "sqlite": cmd_sqlite,
    "export-json": cmd_export_json,
    "pending": cmd_pending,
}


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(1)
    COMMANDS[sys.argv[1]]()


if __name__ == "__main__":
    main()
