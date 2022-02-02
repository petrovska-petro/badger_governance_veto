import pytest
import brownie


# test - an operation can not be executed if it is disputed
def test_execute(deploy, dispute_operation, random_operation):
    id = dispute_operation
    deployer = deploy.deployer
    contract = deploy.contract
    # transaction should revert as it is disputed
    with brownie.reverts(
        "TimelockController: operation is disputed so it can not be executed"
    ):
        contract.execute(
            random_operation.target,
            random_operation.value,
            random_operation.data,
            random_operation.predecessor,
            random_operation.salt,
            {"from": deploy.executor},
        )


# test- if a supreme court decision is true, the operation should be cancelled once veto is passed
def test_veto_passed(deploy, dispute_operation):
    id = dispute_operation
    deployer = deploy.deployer
    contract = deploy.contract
    contract.callDisputeResolve(id, True, "", {"from": deploy.supremecourt})
    # Operation should be cancelled
    assert contract.isOperation(id) == False


# test- if a supreme court decision is false, it should not be disputed after callDisputeResolve
def test_veto_failed(deploy, dispute_operation):
    id = dispute_operation
    deployer = deploy.deployer
    contract = deploy.contract
    contract.callDisputeResolve(id, False, "", {"from": deploy.supremecourt})
    assert contract.getDisputeStatus(id) == 2
