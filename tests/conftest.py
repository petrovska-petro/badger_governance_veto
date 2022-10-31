from brownie import accounts, TimelockController
from dotmap import DotMap
import pytest


@pytest.fixture
def deployer():
    return accounts[0]


@pytest.fixture
def proposer():
    return accounts[1]


@pytest.fixture
def executor():
    return accounts[2]


@pytest.fixture
def veto():
    return accounts[3]


@pytest.fixture
def supremecourt():
    return accounts[4]


@pytest.fixture
def cancellor():
    return accounts[5]


# fixture to deploy TimeController contract
@pytest.fixture()
def timelock(deployer, proposer, executor, veto, supremecourt, cancellor):
    timelock = TimelockController.deploy(
        0,
        [proposer],
        [executor],
        [veto],
        [supremecourt],
        [cancellor],
        {"from": deployer},
    )

    return timelock


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


@pytest.fixture()
def random_second_operation():
    return DotMap(
        target=accounts[7],
        value=0,
        data="0x0e5c011e",
        predecessor=0,
        salt="0xc1059ed2dc130227aa1d1d539ac94c641306905c020436c636e19e3fab56fc7f",
        delay=0,
    )


@pytest.fixture()
def random_broken_operation():
    return DotMap(
        target="0x647eeb5C5ED5A71621183f09F6CE8fa66b96827d",
        value=0,
        data="0x0e5c011e",
        predecessor=0,
        salt="0xc1059ed2dc130227aa1d1d539ac94c641306905c020436c636e19e3fab56fc7f",
        delay=0,
    )


# fixture to schedule an operation
@pytest.fixture()
def schedule_operation(timelock, random_operation, proposer):
    # schedule a proposal
    target = random_operation.target
    value = random_operation.value
    data = random_operation.data
    predecessor = random_operation.predecessor
    salt = random_operation.salt
    delay = random_operation.delay
    timelock.schedule(target, value, data, predecessor, salt, delay, {"from": proposer})
    id = timelock.hashOperation(target, value, data, predecessor, salt)
    return id


# fixture to dispute an operation
@pytest.fixture()
def dispute_operation(timelock, schedule_operation, veto):
    id = schedule_operation
    timelock.callDispute(id, {"from": veto})
    return id
