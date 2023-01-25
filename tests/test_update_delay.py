from brownie import reverts

MIN_DELAY = 172_800
MAX_DELAY = 2_592_000


def test_update_delay_no_allowed_address(timelock, accounts):
    with reverts("TimelockController: caller must be timelock"):
        timelock.updateDelay(8000, {"from": accounts[5]})


def test_update_delay_below_min(timelock):
    with reverts("TimelockController: delay must exceed minimum delay"):
        timelock.updateDelay(MIN_DELAY / 2, {"from": timelock})


def test_update_delay_above_max(timelock):
    with reverts("TimelockController: delay must not exceed maximum delay"):
        timelock.updateDelay(MAX_DELAY * 2, {"from": timelock})


def test_update_delayed_timelock_trigger(timelock):
    NEW_DELAY = MIN_DELAY * 2
    old_delay_val = timelock.getMinDelay()

    tx = timelock.updateDelay(NEW_DELAY, {"from": timelock})

    # assert event
    min_delayed_change_event = tx.events["MinDelayChange"]
    assert len(min_delayed_change_event) > 0
    assert min_delayed_change_event["oldDuration"] == old_delay_val

    # assert update value
    assert timelock.getMinDelay() == NEW_DELAY
