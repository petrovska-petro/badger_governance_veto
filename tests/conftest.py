from brownie import accounts, TimelockController
from dotmap import DotMap
import pytest

# fixture to deploy TimeController contract
@pytest.fixture()
def deploy():
    deployer = accounts[0]
    proposer = accounts[1]
    executor = accounts[2]
    veto = accounts[3]
    supremecourt = accounts[4]
    cancellor = accounts[5]

    deployedTC = TimelockController.deploy(
        0,
        [proposer],
        [executor],
        [veto],
        [supremecourt],
        [cancellor],
        {"from": deployer},
    )
    return DotMap(
        contract=deployedTC,
        deployer=deployer,
        proposer=proposer,
        executor=executor,
        veto=veto,
        supremecourt=supremecourt,
        cancellor=cancellor,
    )


# fixture to create a dummy operation so that we can test callDispute on this operation
@pytest.fixture()
def random_operation():
    # the values I have taken from OpenZepplin tests
    return DotMap(
        target=accounts[6],
        value=0,
        data="0x13e414de",
        predecessor=0,
        salt="0xc1059ed2dc130227aa1d1d539ac94c641306905c020436c636e19e3fab56fc7f",
        delay=0,
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
    contract.schedule(
        target, value, data, predecessor, salt, delay, {"from": deploy.proposer}
    )
    id = contract.hashOperation(target, value, data, predecessor, salt)
    return id


# fixture to dispute an operation
@pytest.fixture()
def dispute_operation(deploy, schedule_operation):
    id = schedule_operation
    contract = deploy.contract
    contract.callDispute(id, {"from": deploy.veto})
    return id
