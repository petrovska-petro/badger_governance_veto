from brownie import (
    accounts,
    TimelockController
)
import brownie
import pytest

def test_flag_operation_role(deploy, schedule_operation):
    id = schedule_operation
    contract = deploy.contract
    with brownie.reverts():
        contract.flagOperation(id, {'from': accounts[2]})

def test_flag_operation_pause(deploy, schedule_operation):
    id = schedule_operation
    contract = deploy.contract
    contract.flagOperation(id, {'from': deploy.proposer})
    assert(contract.getFlagStatus(id)==1)

def test_flag_operation_paused(deploy , schedule_operation):
    id = schedule_operation
    contract = deploy.contract
    contract.flagOperation(id, {'from': deploy.proposer})
    with brownie.reverts("TimelockController: operation is either already paused or can not be paused"):
        contract.flagOperation(id, {'from': deploy.proposer})


