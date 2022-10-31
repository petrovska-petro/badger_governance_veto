from brownie import reverts


def test_resolve_dispute_no_auth(
    timelock, dispute_operation, random_operation, executor, accounts
):
    SUPREMECOURT_ROLE = timelock.SUPREMECOURT_ROLE()
    # dispute the operation
    id = dispute_operation

    # received supereme court judgement as reject
    SUPREME_COURT_REJECT = 1
    revert_msg = f"AccessControl: account {accounts[8].address.lower()} is missing role {SUPREMECOURT_ROLE}"
    with reverts(revert_msg):
        timelock.callDisputeResolve(id, SUPREME_COURT_REJECT, "", {"from": accounts[8]})


def test_resolve_no_disputed(timelock, schedule_operation, supremecourt):
    id = schedule_operation

    SUPREME_COURT_REJECT = 1
    with reverts("TimelockController: operation is not disputed"):
        timelock.callDisputeResolve(
            id, SUPREME_COURT_REJECT, "", {"from": supremecourt}
        )


# test to check that operation should execute once supereme court rejects the veto
def test_execute_after_dispute(
    timelock, dispute_operation, random_operation, executor, supremecourt
):
    # dispute the operation
    id = dispute_operation

    # received supereme court judgement as reject
    SUPREME_COURT_REJECT = 1
    timelock.callDisputeResolve(id, SUPREME_COURT_REJECT, "", {"from": supremecourt})

    # check the operation should not be disputed now
    assert timelock.getDisputeStatus(id) == 2

    # execute the operation
    timelock.execute(
        random_operation.target,
        random_operation.value,
        random_operation.data,
        random_operation.predecessor,
        random_operation.salt,
        {"from": executor},
    )

    # check if the operation is done
    assert timelock.isOperationDone(id) == True


# test to check that operation could not be disputed once veto is failed by supereme court
def test_pause_after_veto_failed(
    timelock, dispute_operation, random_operation, veto, supremecourt
):
    # dispute the operation
    id = dispute_operation

    # received supereme court judgement as reject
    SUPREME_COURT_REJECT = 1
    timelock.callDisputeResolve(id, SUPREME_COURT_REJECT, "", {"from": supremecourt})
    # check the operation should not be disputed now
    assert timelock.getDisputeStatus(id) == 2

    # transaction should revert as the once the veto is failed for one operation that operation can not be disputed again
    with reverts(
        "TimelockController: operation is either already disputed or can not be disputed"
    ):
        timelock.callDispute(id, {"from": veto})


# test the flow of trying to exec a proposed payload without predecessor being exec, needs revert
def test_execution_with_predecessor(
    timelock, random_operation, random_second_operation, proposer, executor
):
    tx = timelock.schedule(
        random_operation.target,
        random_operation.value,
        random_operation.data,
        random_operation.predecessor,
        random_operation.salt,
        random_operation.delay,
        {"from": proposer},
    )

    call_schedule_event = tx.events["CallScheduled"]
    predecessor_id = call_schedule_event["id"]

    timelock.schedule(
        random_second_operation.target,
        random_second_operation.value,
        random_second_operation.data,
        predecessor_id,
        random_second_operation.salt,
        random_second_operation.delay,
        {"from": proposer},
    )

    with reverts("TimelockController: missing dependency"):
        timelock.execute(
            random_second_operation.target,
            random_second_operation.value,
            random_second_operation.data,
            predecessor_id,
            random_second_operation.salt,
            {"from": executor},
        )
