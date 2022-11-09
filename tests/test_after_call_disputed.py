from brownie import reverts, chain


# test - an operation can not be executed if it is disputed
def test_execute(timelock, executor, dispute_operation, random_operation):
    _, block_number = dispute_operation

    block_timestamp = chain[block_number].timestamp
    chain.mine(timestamp=block_timestamp + (random_operation.delay * 2))

    # transaction should revert as it is disputed
    with reverts("TimelockController: operation is disputed so it can not be executed"):
        timelock.execute(
            random_operation.target,
            random_operation.value,
            random_operation.data,
            random_operation.predecessor,
            random_operation.salt,
            {"from": executor},
        )


# test- if a supreme court decision is true, the operation should be cancelled once veto is passed
def test_veto_passed(timelock, supremecourt, dispute_operation):
    id, _ = dispute_operation

    ACCEPT_VETO = 0
    timelock.callDisputeResolve(id, ACCEPT_VETO, "", {"from": supremecourt})

    # Operation should be cancelled
    assert timelock.isOperation(id) == False


# test- if a supreme court decision is false, it should not be disputed after callDisputeResolve
def test_veto_failed(timelock, supremecourt, dispute_operation):
    id, _ = dispute_operation

    REJECT_VETO = 1
    timelock.callDisputeResolve(id, REJECT_VETO, "", {"from": supremecourt})

    assert timelock.getDisputeStatus(id) == 2
