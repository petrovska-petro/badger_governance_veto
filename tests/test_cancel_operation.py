from brownie import reverts


def test_cancel_operation(timelock, schedule_operation, cancellor):
    id = schedule_operation
    tx = timelock.cancel(id, {"from": cancellor})

    cancel_event = tx.events["Cancelled"]
    assert len(cancel_event) > 0
    assert cancel_event["id"] == id and cancel_event["sender"] == cancellor

    assert timelock.getTimestamp(id) == 0


def test_cancel_invalidad_operation(timelock, cancellor):
    with reverts("TimelockController: operation cannot be cancelled"):
        timelock.cancel("0x", {"from": cancellor})


def test_cancel_no_auth(timelock, schedule_operation, accounts):
    id = schedule_operation
    CANCELLOR_ROLE = timelock.CANCELLOR_ROLE()

    revert_msg = f"AccessControl: account {accounts[7].address.lower()} is missing role {CANCELLOR_ROLE}"
    with reverts(revert_msg):
        timelock.cancel(id, {"from": accounts[7]})
