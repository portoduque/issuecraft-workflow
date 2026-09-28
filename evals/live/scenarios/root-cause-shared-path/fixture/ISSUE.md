# Issue: prevent overdrawing transfers

A transfer can currently make the source account balance negative.

Reject a transfer when the source account does not have enough balance. Preserve the existing public behavior for valid operations.
