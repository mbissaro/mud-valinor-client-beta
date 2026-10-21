"""Testa o validador de build.py com um fixture minimo e dados reais."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402


def test_validate_catches_broken_ref_and_duplicate_id() -> None:
    data = {kind: [] for kind in build.TYPES}
    data["region"] = [
        {"id": "region:bri", "name": "Bri", "kind": "city", "sources": ["s"]},
        {"id": "region:bri", "name": "Bri (duplicado)", "kind": "city", "sources": ["s"]},
    ]
    data["location"] = [
        {"id": "loc:bri.praca", "name": "A Praça de Bri", "region": "region:inexistente"},
    ]
    errors, _ = build.validate(data)
    joined = "\n".join(errors)
    assert "id duplicado" in joined
    assert "referencia quebrada" in joined


def test_validate_accepts_minimal_valid_entity() -> None:
    data = {kind: [] for kind in build.TYPES}
    data["region"] = [{"id": "region:bri", "name": "Bri", "kind": "city", "sources": ["s"]}]
    errors, _ = build.validate(data)
    assert errors == []


def test_real_data_has_no_validation_errors() -> None:
    data = build.load_all()
    errors, _ = build.validate(data)
    assert errors == [], "\n".join(errors)


if __name__ == "__main__":
    test_validate_catches_broken_ref_and_duplicate_id()
    test_validate_accepts_minimal_valid_entity()
    try:
        test_real_data_has_no_validation_errors()
    except AssertionError as e:
        print(e)
        sys.exit(1)
    print("Todos os testes passaram.")
