from inspect import signature
from brownie import accounts, TimelockController


def main():
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
    target1 = accounts[6]
    value1 = 0
    signature1 = "set(uint256, uint256, bool)"
    data1 = "0x64482f79000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000001f40000000000000000000000000000000000000000000000000000000000000000"
    predecessor1 = 0
    salt1 = "0xc1059ed2dc130227aa1d1d539ac94c641306905c020436c636e19e3fab56fc7f"
    delay1 = 1
    deployedTC.schedule(
        target1,
        value1,
        # signature1,
        data1,
        predecessor1,
        salt1,
        delay1,
        {"from": proposer},
    )
    target2 = accounts[7]
    value2 = 0
    signature2 = "set(uint256, uint256, bool)"
    data2 = "0x64482f79000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000001f40000000000000000000000000000000000000000000000000000000000000000"
    predecessor2 = 0
    salt2 = "0xc1059ed2dc130227aa1d1d539ac94c641306905c020436c636e19e3fab56fc7f"
    delay2 = 0
    deployedTC.schedule(
        target2,
        value2,
        # signature2,
        data2,
        predecessor2,
        salt2,
        delay2,
        {"from": proposer},
    )
    deployedTC.execute(target2, value2, data2, predecessor2, salt2, {"from": executor})

    target3 = accounts[8]
    value3 = 0
    signature3 = "set(uint256, uint256, bool)"
    data3 = "0x64482f79000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000001f40000000000000000000000000000000000000000000000000000000000000000"
    predecessor3 = 0
    salt3 = "0xc1059ed2dc130227aa1d1d539ac94c641306905c020436c636e19e3fab56fc7f"
    delay3 = 1
    deployedTC.schedule(
        target3,
        value3,
        # signature3,
        data3,
        predecessor3,
        salt3,
        delay3,
        {"from": proposer},
    )
    id = deployedTC.hashOperation(target3, value3, data3, predecessor3, salt3)
    deployedTC.callDispute(id, {"from": veto})
