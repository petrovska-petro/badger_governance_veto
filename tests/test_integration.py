import pytest
import brownie

# test to check that operation should execute once supereme court rejects the veto
def test_execute_after_flag(deploy, flag_operation, random_operation):
    # flag the operation
    id = flag_operation
    deployer = deploy.deployer 
    contract = deploy.contract

    # received supereme court judgement as false
    contract.afterFlagOperation(id , False, {"from": deploy.proposer})

    # check the operation should not be paused now
    assert(contract.getFlagStatus(id)==2)

    # execute the operation
    contract.execute(random_operation.target, random_operation.value, random_operation.data, random_operation.predecessor , random_operation.salt, {"from" : deploy.executer})
    
    # check if the operation is done
    assert(contract.isOperationDone(id)==True)


# test to check that operation could not be paused once veto is failed by supereme court
def test_pause_after_veto_failed(deploy, flag_operation, random_operation):
    # flag the operation
    id = flag_operation
    deployer = deploy.deployer 
    contract = deploy.contract

    # received supereme court judgement as false
    contract.afterFlagOperation(id , False, {"from": deploy.proposer})

    # check the operation should not be paused now
    assert(contract.getFlagStatus(id)==2)

    # transaction should revert as the once the veto is failed for one operation that operation can not be paused again
    with brownie.reverts("TimelockController: operation is either already paused or can not be paused"):
        contract.flagOperation(id, {"from":deploy.veto})



