# GOV.UK Frontend Proposal

## Suggested issue title

`Proposal: explicit processing state guidance for submit buttons and async form actions`

## Suggested issue body

### Summary

I would like to propose clearer GOV.UK Frontend guidance and, if maintainers consider it appropriate, a reusable pattern/API for communicating that a form action is currently being processed.

The problem is most visible on slow networks or slower backend operations: a user activates a submit button and may not receive immediate feedback that the action has been accepted. This can increase uncertainty, repeated activation and cognitive load.

### User need

After activating a form action, users should be able to understand:

- that their action was received
- that the service is still working
- whether they should wait or take another action
- when the action is complete or has failed

This is particularly important for people who benefit from explicit cause-and-effect feedback, including some users with cognitive or learning disabilities.

### Proposed direction

#### 1. Document a processing-state pattern

Provide guidance for a button/form state such as:

- keep the action label understandable, for example `Submitting…`
- prevent accidental repeat submission where the service can safely do so
- use `aria-busy` on an appropriate container when relevant
- announce meaningful state changes to assistive technology without creating repeated/noisy announcements
- preserve progressive enhancement and provide a usable experience if JavaScript is unavailable
- define how errors/timeouts return the interface to an actionable state

The exact markup and ARIA behaviour should be validated through accessibility testing rather than prescribing a spinner alone.

#### 2. Separate visual state from transaction safety

A disabled/loading button is not a substitute for server-side idempotency or duplicate-submission protection. Guidance should make that distinction explicit.

#### 3. Test under delayed responses

A reference example could be tested with artificial response delays and assistive technology to verify:

- keyboard behaviour
- screen-reader announcements
- focus behaviour
- repeated activation
- recovery after request failure
- behaviour without JavaScript

### Scope

I am not proposing a change to how every GOV.UK service validates forms. Validation timing and transaction behaviour are service-specific. The proposal is narrowly about a consistent, accessible way to communicate a processing state when a service has an asynchronous or delayed action.

### Possible first step

Would maintainers be interested in a small prototype/example demonstrating two or three processing-state approaches so they can be compared through accessibility testing before deciding whether this belongs in GOV.UK Frontend or Design System guidance?

I would be happy to help build the prototype and tests following the repository contribution standards.

---

**Author:** SHCHEGLOV NIKOLA  
**Target repository:** https://github.com/alphagov/govuk-frontend/issues