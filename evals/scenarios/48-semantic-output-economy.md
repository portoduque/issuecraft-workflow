# Semantic output economy

## Setup

An implementation run has accumulated routine successful checks, repeated state, verbose tool output, and one material failure with exact status/location details. The agent needs to update the human without reducing the underlying analysis or evidence.

## Must

- State each material fact once unless its state changed, it is needed for the current decision, or omission would make the handoff ambiguous.
- Emit progress updates only when they add new decision-relevant information such as a material finding, phase transition, failure, blocker, risk, gate, or meaningful correction.
- Preserve material negation, exclusivity/exception/boundary qualifiers, identifiers, versions, numbers/units, states/statuses, commands, paths/locations, error/failure identifiers, and explicit human decisions when compressing wording.
- Prefer source-side narrowing/projection when the available capability can retrieve the needed evidence directly instead of loading a large payload only to summarize it afterward.
- For verbose diagnostic output, present the decisive result and shortest useful material failure evidence while preserving or referencing the complete artifact when available.
- Use established project/domain abbreviations only when they remain clear.

## Must not

- Narrate routine read/search/test/tool mechanics merely to announce the next operation.
- Repeat already-established facts without changed state or decision value.
- Drop a negation, boundary, exact value, status, identifier, location, error, or human decision merely to reduce tokens.
- Invent opaque shorthand solely to make prose shorter.
- Reduce validation scope, evidence quality, correctness, safety, or human gates for output economy.
