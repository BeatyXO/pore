from pathlib import Path

from conftest import set_value

CONTRACT = str(Path(__file__).parents[2] / "contracts" / "pore.py")
GEN = 10**18
ZERO = "0x0000000000000000000000000000000000000000"


def test_pore_deploys_and_records_repair_case(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = direct_deploy(CONTRACT)
    direct_vm.sender = direct_alice
    set_value(direct_vm, GEN)
    case_id = contract.create_repair_case(
        direct_bob,
        "Repair leaking roof at unit 4; seal visible leak and replace damaged panel.",
        "Before and after visual evidence must show the same roof area; include a public work report.",
        3600,
        7200,
        ZERO,
        ZERO,
        0,
    )
    assert case_id == 1
    assert '"status": "OPEN"' in contract.get_intent(case_id)


def test_pore_accepts_visual_evidence_kinds(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = direct_deploy(CONTRACT)
    direct_vm.sender = direct_alice
    set_value(direct_vm, GEN)
    case_id = contract.create_repair_case(direct_bob, "Repair item", "Visual before/after proof", 3600, 7200, ZERO, ZERO, 0)
    direct_vm.sender = direct_bob
    contract.submit_repair_evidence(case_id, "IMAGE_URL", "https://example.com/after.jpg", "after photo")
    assert 'IMAGE_URL' in contract.get_evidence(case_id, 0)
