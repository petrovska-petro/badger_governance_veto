from brownie import chain, reverts


def test_batch_schedule_no_auth(timelock, random_operation, accounts):
    PROPOSER_ROLE = timelock.PROPOSER_ROLE()

    revert_msg = f"AccessControl: account {accounts[8].address.lower()} is missing role {PROPOSER_ROLE}"
    with reverts(revert_msg):
        timelock.scheduleBatch(
            [random_operation.target],
            [random_operation.value],
            [random_operation.data],
            random_operation.predecessor,
            random_operation.salt,
            random_operation.delay,
            {"from": accounts[8]},
        )


def test_batch_schedule_min_delay(timelock, random_operation, proposer):
    NEW_DELAY = 5000
    timelock.updateDelay(NEW_DELAY, {"from": timelock})

    with reverts("TimelockController: insufficient delay"):
        timelock.scheduleBatch(
            [random_operation.target],
            [random_operation.value],
            [random_operation.data],
            random_operation.predecessor,
            random_operation.salt,
            NEW_DELAY - 500,
            {"from": proposer},
        )


def test_batch_schedule_mismatch_length(timelock, random_operation, proposer):
    # diff target lenght != value
    with reverts("TimelockController: length mismatch"):
        timelock.scheduleBatch(
            [random_operation.target, random_operation.target],
            [random_operation.value],
            [random_operation.data],
            random_operation.predecessor,
            random_operation.salt,
            0,
            {"from": proposer},
        )

    # diff target lenght != data
    with reverts("TimelockController: length mismatch"):
        timelock.scheduleBatch(
            [random_operation.target, random_operation.target],
            [random_operation.value, random_operation.value],
            [random_operation.data],
            random_operation.predecessor,
            random_operation.salt,
            0,
            {"from": proposer},
        )


def test_batch_schedule_same_operation(timelock, random_operation, proposer):
    timelock.scheduleBatch(
        [random_operation.target],
        [random_operation.value],
        [random_operation.data],
        random_operation.predecessor,
        random_operation.salt,
        0,
        {"from": proposer},
    )

    with reverts("TimelockController: operation already scheduled"):
        timelock.scheduleBatch(
            [random_operation.target],
            [random_operation.value],
            [random_operation.data],
            random_operation.predecessor,
            random_operation.salt,
            0,
            {"from": proposer},
        )


def test_batch_schedule(timelock, random_operation, random_second_operation, proposer):
    tx = timelock.scheduleBatch(
        [random_operation.target, random_second_operation.target],
        [random_operation.value, random_second_operation.value],
        [random_operation.data, random_second_operation.data],
        random_operation.predecessor,
        random_operation.salt,
        0,
        {"from": proposer},
    )

    block_timestamp = chain[tx.block_number].timestamp
    schedule_events = tx.events["CallScheduled"]
    # queue 2 targets/actions
    assert len(schedule_events) > 1

    for event in schedule_events:
        id = event["id"]
        assert timelock.getTimestamp(id) == block_timestamp


def test_batch_execution_no_schedule(timelock, random_operation, executor):
    with reverts("TimelockController: operation is not ready"):
        timelock.executeBatch(
            [random_operation.target],
            [random_operation.value],
            [random_operation.data],
            random_operation.predecessor,
            random_operation.salt,
            {"from": executor},
        )


def test_batch_execution_early(timelock, random_operation, proposer, executor):
    NEW_DELAY = 5000
    timelock.updateDelay(NEW_DELAY, {"from": timelock})

    tx = timelock.scheduleBatch(
        [random_operation.target],
        [random_operation.value],
        [random_operation.data],
        random_operation.predecessor,
        random_operation.salt,
        NEW_DELAY,
        {"from": proposer},
    )

    block_timestamp = chain[tx.block_number].timestamp
    chain.mine(timestamp=block_timestamp + (NEW_DELAY / 2))

    with reverts("TimelockController: operation is not ready"):
        timelock.executeBatch(
            [random_operation.target],
            [random_operation.value],
            [random_operation.data],
            random_operation.predecessor,
            random_operation.salt,
            {"from": executor},
        )

    # mining further to test exec
    chain.mine(timestamp=block_timestamp + NEW_DELAY)

    timelock.executeBatch(
        [random_operation.target],
        [random_operation.value],
        [random_operation.data],
        random_operation.predecessor,
        random_operation.salt,
        {"from": executor},
    )


def test_batch_execution_no_auth(timelock, random_operation, proposer, accounts):
    EXECUTOR_ROLE = timelock.EXECUTOR_ROLE()

    timelock.scheduleBatch(
        [random_operation.target],
        [random_operation.value],
        [random_operation.data],
        random_operation.predecessor,
        random_operation.salt,
        0,
        {"from": proposer},
    )

    revert_msg = f"AccessControl: account {accounts[8].address.lower()} is missing role {EXECUTOR_ROLE}"
    with reverts(revert_msg):
        timelock.executeBatch(
            [random_operation.target],
            [random_operation.value],
            [random_operation.data],
            random_operation.predecessor,
            random_operation.salt,
            {"from": accounts[8]},
        )


def test_batch_execution_mismatch_length(
    timelock, random_operation, random_second_operation, proposer, executor
):
    timelock.scheduleBatch(
        [random_operation.target, random_second_operation.target],
        [random_operation.value, random_second_operation.value],
        [random_operation.data, random_second_operation.data],
        random_operation.predecessor,
        random_operation.salt,
        0,
        {"from": proposer},
    )

    # diff target lenght != value
    with reverts("TimelockController: length mismatch"):
        timelock.executeBatch(
            [random_operation.target, random_operation.target],
            [random_operation.value],
            [random_operation.data],
            random_operation.predecessor,
            random_operation.salt,
            {"from": executor},
        )

    # diff target lenght != data
    with reverts("TimelockController: length mismatch"):
        timelock.executeBatch(
            [random_operation.target, random_operation.target],
            [random_operation.value, random_operation.value],
            [random_operation.data],
            random_operation.predecessor,
            random_operation.salt,
            {"from": executor},
        )


def test_batch_execution_tx_revert(
    timelock, random_broken_operation, proposer, executor
):
    timelock.scheduleBatch(
        [random_broken_operation.target],
        [random_broken_operation.value],
        [random_broken_operation.data],
        random_broken_operation.predecessor,
        random_broken_operation.salt,
        0,
        {"from": proposer},
    )

    with reverts("TimelockController: underlying transaction reverted"):
        timelock.executeBatch(
            [random_broken_operation.target],
            [random_broken_operation.value],
            [random_broken_operation.data],
            random_broken_operation.predecessor,
            random_broken_operation.salt,
            {"from": executor},
        )


def test_batch_execution(
    timelock, random_operation, random_second_operation, proposer, executor
):
    timelock.scheduleBatch(
        [random_operation.target, random_second_operation.target],
        [random_operation.value, random_second_operation.value],
        [random_operation.data, random_second_operation.data],
        random_operation.predecessor,
        random_operation.salt,
        0,
        {"from": proposer},
    )

    tx = timelock.executeBatch(
        [random_operation.target, random_second_operation.target],
        [random_operation.value, random_second_operation.value],
        [random_operation.data, random_second_operation.data],
        random_operation.predecessor,
        random_operation.salt,
        {"from": executor},
    )

    call_executed_events = tx.events["CallExecuted"]
    assert len(call_executed_events) > 1

    for event in call_executed_events:
        id = event["id"]
        assert timelock.getTimestamp(id) == 1
