from brownie import (
    accounts,
    TimelockController
)
import brownie
import pytest

def test_flag_operation(deploy, schedule_operation):
    id = schedule_operation
    deployer = deploy.deployer 
    contract = deploy.contract
    contract.flagOperation(id, {'from': deployer})
    assert(contract.getOperationState(id)==1)

def test_flag_operation_paused(deploy , schedule_operation):
    id = schedule_operation
    deployer = deploy.deployer 
    contract = deploy.contract
    contract.flagOperation(id, {'from': deployer})
    with brownie.reverts():
        contract.flagOperation(id, {'from': deployer})


