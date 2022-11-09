from brownie import reverts


def test_grant_role_no_auth(timelock, accounts):
    EXECUTOR_ROLE = timelock.EXECUTOR_ROLE()
    TIMELOCK_ADMIN_ROLE = timelock.TIMELOCK_ADMIN_ROLE()

    revert_msg = f"AccessControl: account {accounts[8].address.lower()} is missing role {TIMELOCK_ADMIN_ROLE}"
    with reverts(revert_msg):
        timelock.grantRole(EXECUTOR_ROLE, accounts[7], {"from": accounts[8]})


def test_gran_role_admin(timelock, accounts):
    EXECUTOR_ROLE = timelock.EXECUTOR_ROLE()

    tx = timelock.grantRole(EXECUTOR_ROLE, accounts[6], {"from": timelock})

    granted_role_event = tx.events["RoleGranted"]
    assert len(granted_role_event) > 0
    assert (
        granted_role_event["role"] == EXECUTOR_ROLE
        and granted_role_event["account"] == accounts[6]
    )

    assert timelock.hasRole(EXECUTOR_ROLE, accounts[6])


def test_revoke_role_assigned(timelock, executor):
    EXECUTOR_ROLE = timelock.EXECUTOR_ROLE()

    tx = timelock.revokeRole(EXECUTOR_ROLE, executor, {"from": timelock})

    role_revoked_event = tx.events["RoleRevoked"]
    assert len(role_revoked_event) > 0
    assert (
        role_revoked_event["role"] == EXECUTOR_ROLE
        and role_revoked_event["account"] == executor
    )

    assert timelock.hasRole(EXECUTOR_ROLE, executor) == False


def test_renounce_role_no_auth(timelock, executor, accounts):
    EXECUTOR_ROLE = timelock.EXECUTOR_ROLE()

    with reverts("AccessControl: can only renounce roles for self"):
        timelock.renounceRole(EXECUTOR_ROLE, executor, {"from": accounts[5]})


def test_renounce_role_for_self(timelock, executor):
    EXECUTOR_ROLE = timelock.EXECUTOR_ROLE()

    timelock.renounceRole(EXECUTOR_ROLE, executor, {"from": executor})

    assert timelock.hasRole(EXECUTOR_ROLE, executor) == False
