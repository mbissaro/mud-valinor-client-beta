"""Testa o validador de build.py com um fixture minimo e dados reais."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402
import minerar  # noqa: E402


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


def test_minerar_separa_titulo_descricao_objetos_e_mobs() -> None:
    # formato SMAUG: titulo \r\n, descricao \n\r, objeto \r\n, mob \n\r, jogador e fala ignorados
    raw = ("<20hp 100m 99mv> (Seguro) A Praça\r\n"
           "Uma praça grande.\n\rCom uma fonte.\n\rSaídas: n s\r\n"
           "Uma fonte jorra água.\r\n"
           "Beltrano de Bri, o Aprendiz, está em pé aqui.\r\n"
           "Um guarda patrulha aqui.\n\r"
           "O guarda disse 'Olá!'\r\n\r\n")
    rooms, visits, _ = minerar.parse_rooms(raw, set())
    (r,) = rooms.values()
    assert r["title"] == "A Praça" and r["safe"]
    assert r["description"] == "Uma praça grande.\nCom uma fonte."
    assert list(r["objects"]) == ["Uma fonte jorra água."]
    assert list(r["mobs"]) == ["Um guarda patrulha aqui."]
    assert list(r["exits"]) == ["n s"] and len(visits) == 1


if __name__ == "__main__":
    test_minerar_separa_titulo_descricao_objetos_e_mobs()
    test_validate_catches_broken_ref_and_duplicate_id()
    test_validate_accepts_minimal_valid_entity()
    try:
        test_real_data_has_no_validation_errors()
    except AssertionError as e:
        print(e)
        sys.exit(1)
    print("Todos os testes passaram.")
