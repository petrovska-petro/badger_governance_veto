from brownie import (
    accounts,
    TimelockController
)
from dotmap import DotMap 
import pytest
# fixture to deploy TimeController contract
@pytest.fixture()
def deploy():
    deployer = accounts[0]
    deployedTC = TimelockController.deploy(0, [deployer], [deployer], [deployer], {'from': deployer})
    return DotMap(
        contract = deployedTC,
        deployer = deployer,
        proposer = deployer,
        executer = deployer,
        veto = deployer
    )

# fixture to create a dummy operation so that we can test flagOperation on this operation
@pytest.fixture()
def random_operation():
    return DotMap(
        target = accounts[1],
        value = 10,
        data = "",
        predecessor = "",
        salt = "",
        delay = 0 
    )

# fixture to schedule an operation
@pytest.fixture()
def schedule_operation(deploy, random_operation):
    contract = deploy.contract
    # schedule a proposal
    target = random_operation.target
    value = random_operation.value
    data = random_operation.data
    predecessor = random_operation.predecessor
    salt = random_operation.salt
    delay = random_operation.delay
    contract.schedule(target, value, data, predecessor, salt, delay, {'from': deploy.proposer})
    id = contract.hashOperation(target, value, data, predecessor, salt)
    return id 