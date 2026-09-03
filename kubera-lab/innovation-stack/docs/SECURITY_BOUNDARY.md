# DZAMBALA Security Boundary

The public reference runtime is currently a **single-process reference implementation**, not a process-isolation or sandbox boundary. Stronger process/container isolation can be added later, but today safety depends on capability discipline: agents and plugins should receive `SovereignToolExecutor`, not raw provider clients or credentials.

`ToolAdapter.execute()` receives only tool identity, operation, target and the finalized sanitized arguments. It must never receive the `AuthorizationSigner`, signing secret, grant verification internals or governance objects.

The canonical operational audit remains `EvidenceLedger`. A `CONFIRMED_SUCCEEDED` action record is written by `SovereignToolExecutor` only after the adapter returned and the idempotency reservation was completed. If the external action may have happened but local completion/evidence is uncertain, the executor returns `UNKNOWN_EXTERNAL_STATE` and must not blindly retry.

This boundary does not claim protection against arbitrary code that already possesses raw provider credentials. Production deployments must keep those credentials outside agent/plugin reach and add stronger isolation as required.
