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
    target = accounts[6]
    value = 0
    data = "0x13e414de"
    predecessor = 0
    salt = "0xc1059ed2dc130227aa1d1d539ac94c641306905c020436c636e19e3fab56fc7f"
    delay = 0
    deployedTC.schedule(
        target, value, data, predecessor, salt, delay, {"from": proposer}
    )
