# KUBERA Stones — System Design

## Product architecture

KUBERA Stones is a hybrid physical/digital workflow. The digital layer structures customer intent, configuration, evidence and fulfillment; the maker remains the final design and fabrication authority.

```text
CUSTOMER
  -> conversation / form
  -> structured commission input
  -> constraint validation
  -> design brief
  -> maker feasibility gate
  -> build specification
  -> fabrication
  -> quality checkpoint
  -> provenance package
  -> fulfillment
```

## Domain objects

### Commission
Represents one customer request and its lifecycle.

### Configuration
A versioned snapshot of customer-selected and maker-approved parameters.

### MaterialSet
Records natural stone, optional coin/gemstone/collectible components and material notes.

### BuildSpecification
The maker-approved interpretation of the configuration. This is the authoritative production record.

### ProvenanceRecord
Links the final artifact to the approved build specification, completion evidence and ownership/fulfillment record.

## State model

```text
DRAFT
  -> CUSTOMER_INPUT_COMPLETE
  -> MAKER_REVIEW
  -> FEASIBLE | REVISION_REQUIRED | DECLINED
  -> BUILD_SPEC_APPROVED
  -> IN_PRODUCTION
  -> QUALITY_REVIEW
  -> COMPLETED
  -> FULFILLED
```

## Guardrails

1. Customer inputs are not production instructions until maker approval.
2. Natural-material variation is expected and recorded.
3. Customer-supplied collectibles require suitability and ownership confirmation.
4. Symbolic references are descriptive design inputs, not outcome guarantees.
5. Shipping eligibility is evaluated before final fulfillment commitment.
6. Proprietary fabrication methods stay outside the public repository.

## Digital traceability

A future implementation can hash each approved configuration and final provenance record so the physical piece has a tamper-evident digital history without exposing private customer data.

Suggested record chain:

```text
commission_id
  -> configuration_hash
  -> build_spec_hash
  -> completion_evidence_hash
  -> provenance_record
```

## KUBERA integration opportunity

A bounded KUBERA Agent can assist only with pre-production information handling:

- convert customer conversation into structured fields;
- detect missing configuration data;
- prepare a maker-review brief;
- prepare status updates;
- generate fulfillment checklists;
- create a provenance draft.

It must not autonomously approve feasibility, material suitability, final symbolism, fabrication or shipment.
