from brownie import (
    accounts,
    TimelockController
)
import brownie
import pytest

# test only veto can Flag the Operation
def test_flag_operation_role(deploy, schedule_operation):
    id = schedule_operation
    contract = deploy.contract
    # the transaction should revert as it is not getting called from veto
    with brownie.reverts():
        contract.flagOperation(id, {'from': accounts[2]})

# test to check if an operation is paused after it is flagged
def test_flag_operation_pause(deploy, schedule_operation):
    id = schedule_operation
    contract = deploy.contract
    contract.flagOperation(id, {'from': deploy.proposer})
    assert(contract.getFlagStatus(id)==1)

# test- an operation is paused it can not be paused
def test_flag_operation_paused(deploy , schedule_operation):
    id = schedule_operation
    contract = deploy.contract
    contract.flagOperation(id, {'from': deploy.proposer})
    # transaction should revert as it is already paused
    with brownie.reverts("TimelockController: operation is either already paused or can not be paused"):
        contract.flagOperation(id, {'from': deploy.proposer})


