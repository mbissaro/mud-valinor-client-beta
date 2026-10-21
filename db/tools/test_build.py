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


def test_minerar_itens_de_inventario_npc_loja_e_eventos() -> None:
    lines = ["Você está carregando:", "     (2x) um pão bem recheado para viagem", "",
             "O guarda está usando:", "<como luz>        uma tocha", "",
             "Núm    Nível    Quant    Item                                           Preço",
             " 1         7     Ilim.    um par de manoplas de ferro                        3", "",
             "Você pegou um canino de morcego do corpo de um morcego peludo.",
             "Você colocou um protetor de ferro para os braços em seus braços.",
             "O professor Elundhir deu um pão bem recheado para viagem para você."]
    items = minerar.parse_items(lines, ["room:x"] * len(lines), "O guarda patrulha")
    pao = items["um pão bem recheado para viagem"]
    assert pao["held"] == 2 and pao["verbs"]["recebeu"] == 1
    assert items["uma tocha"]["worn_by"] == {"O guarda <como luz>"}
    assert items["um par de manoplas de ferro"]["shops"]["room:x"]["price"] == 3
    assert items["um canino de morcego"]["dropped_by"] == {"um morcego peludo"}
    assert "um protetor de ferro para os braços" in items


if __name__ == "__main__":
    test_minerar_itens_de_inventario_npc_loja_e_eventos()
    test_minerar_separa_titulo_descricao_objetos_e_mobs()
    test_validate_catches_broken_ref_and_duplicate_id()
    test_validate_accepts_minimal_valid_entity()
    try:
        test_real_data_has_no_validation_errors()
    except AssertionError as e:
        print(e)
        sys.exit(1)
    print("Todos os testes passaram.")
