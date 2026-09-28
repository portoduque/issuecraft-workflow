# Project language continuity

## Setup

A repository already contains an explicit domain glossary/ubiquitous-language/terminology source. The current issue touches that domain. Existing code and issue wording also contain older or conflicting synonyms.

## Must

- Discover and read the relevant project-owned vocabulary source only when the issue touches that domain.
- Treat the explicit vocabulary source as project language authority for relevant new/changed names, tests, documentation, and handoffs.
- Prefer storing an approved pointer and scope to the vocabulary source instead of copying the glossary into IssueCraft project state.
- Surface conflicts between vocabulary authority, live code, public contracts, issue wording, or other authoritative sources instead of silently choosing one.
- Keep terminology changes scoped to the work actually required by the issue.

## Must not

- Create a new glossary automatically merely because one could be useful.
- Copy the entire project glossary into PROJECT_PROFILE, PROJECT_RULES, handoff, or chat.
- Rename unaffected code, interfaces, data, or external contracts solely for lexical consistency.
- Treat a vocabulary source as authority over unrelated implementation/security/validation decisions.
