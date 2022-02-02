from brownie import accounts, TimelockController
import brownie
import pytest

# test only veto can dispute the Operation
def test_dispute_operation_role(deploy, schedule_operation):
    id = schedule_operation
    contract = deploy.contract
    # the transaction should revert as it is not getting called from veto
    with brownie.reverts():
        contract.callDispute(id, {"from": deploy.executor})


# test to check if an operation is disputed after it is Disputed
def test_dispute_operation_pause(deploy, schedule_operation):
    id = schedule_operation
    contract = deploy.contract
    contract.callDispute(id, {"from": deploy.veto})
    assert contract.getDisputeStatus(id) == 1


# test- an operation is disputed it can not be disputed
def test_dispute_operation_disputed(deploy, schedule_operation):
    id = schedule_operation
    contract = deploy.contract
    contract.callDispute(id, {"from": deploy.veto})
    # transaction should revert as it is already disputed
    with brownie.reverts(
        "TimelockController: operation is either already disputed or can not be disputed"
    ):
        contract.callDispute(id, {"from": deploy.veto})
