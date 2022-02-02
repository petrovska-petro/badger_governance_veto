# badger_governance_veto

## Overview 

The timelock is based on the OpenZeppelin timelock controller.

For a deep explanation of the TimelockController, read [TimelockController](https://docs.openzeppelin.com/contracts/4.x/api/governance#TimelockController)

In addition to the PROPOSE_ROLE and EXECUTE_ROLE that exist on the TimelockController, we should have a VETO_ROLE. The admin permissions for this role are the same as the others.

A vetoer can dispute a proposal once proposed, but before it is executed.

Once vetoed, a proposal is ‘disputed’ and cannot be executed. The veto should notify another contract, the Supreme Court, that a proposal is disputed and that it requires additional input.

## Source code changes
 1. Added VETO_ROLE.
 2. Added SUPREMECOURT_ROLE.
 3. Added CANCELLOR_ROLE.
 4. Initialized all roles in constructor.
 5. Created a mapping called disputed which tells state of operations.
 * 0- not disputed can be disputed.
 * 1- disputed operation.
 * 2- not disputed but can not be disputed, needed supreme court rejects it once.
 6. Created a Function called callDispute to dispute operation.
 7. Created an event CallDisputed, will emit after the operation is Disputed.
 8. Created a Function callDisputeResolve, which will take the supreme court's judgement as input. It will either unpause the operation or cancel it based upon judgement.
 9. Created an event CallDisputedResolved, will emit after the disputed operation is resolved.
 10. Updated beforeCall() function so that the disputed operation can not be executed. 
