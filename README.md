# badger_governance_veto

## Overview 

The timelock is based on the OpenZeppelin timelock controller.

For a deep explanation of the TimelockController, read [TimelockController](https://docs.openzeppelin.com/contracts/4.x/api/governance#TimelockController)

In addition to the PROPOSE_ROLE and EXECUTE_ROLE that exist on the TimelockController, we should have a VETO_ROLE. The admin permissions for this role are the same as the others.

A vetoer can flag a proposal once proposed, but before it is executed.

Once vetoed, a proposal is ‘paused’ and cannot be executed. The veto should notify another contract, the Supreme Court, that a proposal is disputed and that it requires additional input.

## Source code changes
 1. Added VETO_ROLE.
 2. Initialized VETO_ROLE in constructor.
 3. Created a mapping called paused which tells state of operations.
 * 0- not paused can be paused.
 * 1- paused operation.
 * 2- not paused but can not be paused, needed supreme court rejects it once.
 4. Created a Function called FlagOperation to flag operation.
 5. Created an event FlaggedOperation, will emit after the operation is flagged.
 6. Created a Function afterFlagOperation, which will take the supreme court's judgement as input. It will either unpause the operation or cancel it based upon judgement.
 7. Updated beforeCall() function so that the paused operation can not be executed. 
