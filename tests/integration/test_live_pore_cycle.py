import json
import os
from pathlib import Path

from gltest import get_validator_factory
from gltest.accounts import get_accounts
from gltest.contracts.contract_factory import ContractFactory
import gltest.contracts.contract as contract_module
import inspect
from gltest.assertions import tx_execution_succeeded
from gltest_cli.config.general import get_general_config


CONTRACT = "EvidenceGatedIntentEscrow"
DEPLOYED_ADDRESS = "0x9232E691658D6B3Bb04c36857dDBe86fcC7341B6"
ZERO = "0x0000000000000000000000000000000000000000"
GEN = 10**16


def context(verdict="SATISFIED", ok=True, completed=None):
    vf = get_validator_factory()
    validators = vf.batch_create_mock_validators(count=5, mock_llm_response={
        "nondet_exec_prompt": {"GenLayer validator judging evidence": json.dumps({
            "ok": ok, "verdict": verdict, "reason": "repair evidence supports completion",
            "evidence_summary": "before and after evidence inspected", "missing_requirements": "", "safe_error": "",
            "completed_deliverables": completed or []
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
    opened = contract.create_repair_case(args=[fulfiller, "Repair leaking roof at unit 4", "Before and after visual proof", '[{"id":"roof","weight_bps":6000},{"id":"panel","weight_bps":4000}]', 1800, 1800, ZERO, ZERO, 0]).transact(value=GEN, transaction_context=context())
    assert tx_execution_succeeded(opened)
    evidence = contract.submit_repair_evidence(args=[base, "TEXT", "Roof sealed and visible leak repaired; panel remains pending.", "repair report"]).transact(transaction_context=context())
    assert tx_execution_succeeded(evidence)
    resolved = contract.resolve(args=[base]).transact(transaction_context=context("PARTIAL", True, ["roof"]))
    assert tx_execution_succeeded(resolved)
    assert contract.verdict_of(args=[base]).call() == "PARTIAL"
    result = json.loads(contract.get_intent(args=[base]).call())
    assert result["payout_to_requester"] == str(GEN * 4000 // 10000)
    assert result["payout_to_fulfiller"] == str(GEN * 6000 // 10000)


def test_live_mutual_split_requires_exact_same_bps(default_account):
    accounts = [a for a in get_accounts() if a.address != default_account.address]
    assert accounts, "a second configured test account is required"
    repairer = accounts[0]
    factory = ContractFactory(CONTRACT, Path("contracts/pore.py").read_text())
    requester_contract = factory.build_contract(contract_address=DEPLOYED_ADDRESS, account=default_account).connect(default_account)
    base = int(json.loads(requester_contract.stats(args=[]).call())["next_intent_id"])
    opened = requester_contract.create_repair_case(args=[repairer.address, "Repair panel", "Evidence required", '[{"id":"panel","weight_bps":10000}]', 1800, 1800, ZERO, ZERO, 0]).transact(value=GEN, transaction_context=context())
    assert tx_execution_succeeded(opened)
    evidence = requester_contract.submit_repair_evidence(args=[base, "TEXT", "ambiguous repair report", "review required"]).transact(transaction_context=context())
    assert tx_execution_succeeded(evidence)
    unresolved = requester_contract.resolve(args=[base]).transact(transaction_context=context("INCONCLUSIVE", False))
    assert tx_execution_succeeded(unresolved)
    requester_approval = requester_contract.accept_mutual_repair_settlement(args=[base, 5000]).transact(transaction_context=context())
    assert tx_execution_succeeded(requester_approval)
    repairer_contract = factory.build_contract(contract_address=DEPLOYED_ADDRESS, account=repairer).connect(repairer)
    mismatch = repairer_contract.accept_mutual_repair_settlement(args=[base, 6000]).transact(transaction_context=context())
    assert not tx_execution_succeeded(mismatch)
    final = repairer_contract.accept_mutual_repair_settlement(args=[base, 5000]).transact(transaction_context=context())
    assert tx_execution_succeeded(final)
