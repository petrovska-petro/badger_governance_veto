from brownie import (
    accounts,
    TimelockController
)
from dotmap import DotMap 
import pytest

@pytest.fixture()
def deploy():
    deployer = accounts[0]
    deployedTC = TimelockController.deploy(10, [deployer], [deployer], [deployer], {'from': deployer})
    return DotMap(
        contract = deployedTC,
        deployer = deployer 
    )

@pytest.fixture()
def random_operation():
    return DotMap(
        target = accounts[1],
        value = 10,
        data = "",
        predecessor = "",
        salt = "",
        delay = 100 
    )

@pytest.fixture()
def schedule_operation(deploy, random_operation):
    deployer = deploy.deployer 
    contract = deploy.contract
    # schedule a proposal
    target = random_operation.target
    value = random_operation.value
    data = random_operation.data
    predecessor = random_operation.predecessor
    salt = random_operation.salt
    delay = random_operation.delay
    contract.schedule(target, value, data, predecessor, salt, delay, {'from': deployer})
    id = contract.hashOperation(target, value, data, predecessor, salt)
    return id 