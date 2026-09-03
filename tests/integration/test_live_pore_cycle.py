import json
import os
from pathlib import Path

from gltest import get_validator_factory
from gltest.contracts.contract_factory import ContractFactory
import gltest.contracts.contract as contract_module
import inspect
from gltest.assertions import tx_execution_succeeded
from gltest_cli.config.general import get_general_config


CONTRACT = "EvidenceGatedIntentEscrow"
DEPLOYED_ADDRESS = "0x4A8D16452061f130FF9915138d064Ff3B69811cb"
ZERO = "0x0000000000000000000000000000000000000000"
GEN = 10**16


def context(verdict="SATISFIED", ok=True):
    vf = get_validator_factory()
    validators = vf.batch_create_mock_validators(count=5, mock_llm_response={
        "nondet_exec_prompt": {"GenLayer validator judging evidence": json.dumps({
            "ok": ok, "verdict": verdict, "reason": "repair evidence supports completion",
            "evidence_summary": "before and after evidence inspected", "missing_requirements": "", "safe_error": ""
        })}
    })
    return {"validators": [v.to_dict() for v in validators]}


def test_live_create_evidence_resolve_cycle(default_account):
    os.chdir(Path(__file__).parents[2])
    get_general_config().set_contracts_dir(Path("contracts").resolve())
    factory = ContractFactory(CONTRACT, Path("contracts/pore.py").read_text())
    contract = factory.build_contract(contract_address=DEPLOYED_ADDRESS, account=default_account).connect(default_account)
    # gltest 0.3.0-rc7 passes a deprecated `fees` kwarg to the installed client;
    # value-bearing transactions themselves are supported by the client.
    contract_module._fee_kwargs = lambda call, fees, fee_value: {}
    client = contract_module.get_gl_client()
    original_wait = client.wait_for_transaction_receipt
    wait_params = inspect.signature(original_wait).parameters
    if "wait_until" not in wait_params:
        client.wait_for_transaction_receipt = lambda transaction_hash, interval, retries, **kwargs: original_wait(transaction_hash, interval=interval, retries=retries)
    fulfiller = default_account.address
    base = int(json.loads(contract.stats(args=[]).call())["next_intent_id"])
    opened = contract.create_repair_case(args=[fulfiller, "Repair leaking roof at unit 4", "Before and after visual proof", 1800, 1800, ZERO, ZERO, 0]).transact(value=GEN, transaction_context=context())
    assert tx_execution_succeeded(opened)
    evidence = contract.submit_repair_evidence(args=[base, "AFTER_PHOTO", "https://example.com/after.jpg", "after repair photo"]).transact(transaction_context=context())
    assert tx_execution_succeeded(evidence)
    resolved = contract.resolve(args=[base]).transact(transaction_context=context())
    assert tx_execution_succeeded(resolved)
    assert contract.verdict_of(args=[base]).call() == "SATISFIED"
