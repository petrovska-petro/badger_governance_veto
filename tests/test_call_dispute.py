from brownie import reverts

# test only veto can dispute the Operation
def test_dispute_operation_role(timelock, schedule_operation, executor):
    id = schedule_operation
    # the transaction should revert as it is not getting called from veto
    with reverts():
        timelock.callDispute(id, {"from": executor})


# test to check if an operation is disputed after it is Disputed
def test_dispute_operation_pause(timelock, schedule_operation, veto):
    id = schedule_operation
    timelock.callDispute(id, {"from": veto})
    assert timelock.getDisputeStatus(id) == 1


# test- an operation is disputed it can not be disputed
def test_dispute_operation_disputed(timelock, schedule_operation, veto):
    id = schedule_operation
    timelock.callDispute(id, {"from": veto})
    # transaction should revert as it is already disputed
    with reverts(
        "TimelockController: operation is either already disputed or can not be disputed"
    ):
        timelock.callDispute(id, {"from": veto})


# test- an operation is disputed when does not exist
def test_dispute_non_existent_operation(timelock, veto):
    with reverts(
        "TimelockController: operation is either done or does not exist, can not be disputed"
    ):
        timelock.callDispute("0x", {"from": veto})
