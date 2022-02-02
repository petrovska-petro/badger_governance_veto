import pytest
import brownie

# test to check that operation should execute once supereme court rejects the veto
def test_execute_after_dispute(deploy, dispute_operation, random_operation):
    # dispute the operation
    id = dispute_operation
    deployer = deploy.deployer 
    contract = deploy.contract

    # received supereme court judgement as false
    contract.afterCallDisputed(id , False, "", {"from": deploy.supremecourt})

    # check the operation should not be disputed now
    assert(contract.getDisputeStatus(id)==2)

    # execute the operation
    contract.execute(random_operation.target, random_operation.value, random_operation.data, random_operation.predecessor , random_operation.salt, {"from" : deploy.executor})
    
    # check if the operation is done
    assert(contract.isOperationDone(id)==True)


# test to check that operation could not be disputed once veto is failed by supereme court
def test_pause_after_veto_failed(deploy, dispute_operation, random_operation):
    # dispute the operation
    id = dispute_operation
    deployer = deploy.deployer 
    contract = deploy.contract

    # received supereme court judgement as false
    contract.afterCallDisputed(id , False, "", {"from": deploy.supremecourt})

    # check the operation should not be disputed now
    assert(contract.getDisputeStatus(id)==2)

    # transaction should revert as the once the veto is failed for one operation that operation can not be disputed again
    with brownie.reverts("TimelockController: operation is either already disputed or can not be disputed"):
        contract.callDispute(id, {"from":deploy.veto})



