from brownie import reverts


def test_update_delay_no_allowed_address(timelock, accounts):
    with reverts("TimelockController: caller must be timelock"):
        timelock.updateDelay(8000, {"from": accounts[5]})


def test_update_delayed_timelock_trigger(timelock):
    NEW_DELAY = 10_000
    old_delay_val = timelock.getMinDelay()

    tx = timelock.updateDelay(NEW_DELAY, {"from": timelock})

    # assert event
    min_delayed_change_event = tx.events["MinDelayChange"]
    assert len(min_delayed_change_event) > 0
    assert min_delayed_change_event["oldDuration"] == old_delay_val

    # assert update value
    assert timelock.getMinDelay() == NEW_DELAY
