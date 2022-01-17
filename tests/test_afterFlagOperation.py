import pytest
import brownie
@pytest.fixture()
def flag_operation(deploy, schedule_operation):
    id = schedule_operation
    deployer = deploy.deployer 
    contract = deploy.contract
    contract.flagOperation(id, {'from': deployer})
    return id 

def test_execute(deploy, flag_operation, random_operation):
    id = flag_operation
    deployer = deploy.deployer 
    contract = deploy.contract

    with brownie.reverts():
        contract.execute(random_operation.target, random_operation.value, random_operation.data, random_operation.salt, random_operation.delay)

def test_veto_passed(deploy, flag_operation):
    id = flag_operation
    deployer = deploy.deployer 
    contract = deploy.contract
    contract.afterFlagOperation(id , True)
    assert(contract.getFlagStatus(id)==1)

def test_veto_failed(deploy , flag_operation):
    id = flag_operation
    deployer = deploy.deployer 
    contract = deploy.contract
    contract.afterFlagOperation(id , False)
    assert(contract.getFlagStatus(id)==2)
