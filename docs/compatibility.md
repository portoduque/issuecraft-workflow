# Agent Compatibility

The workflow uses the open Agent Skills pattern and keeps agent-specific details out of the canonical core.

## Codex

Repository skills are discovered under `.agents/skills/<skill>/SKILL.md`. Explicit invocation uses a skill mention such as `$implement-issue`; implicit invocation can also match the skill description.

Official reference: https://developers.openai.com/codex/skills

## Claude Code

Project skills are discovered under `.claude/skills/<skill>/SKILL.md`. A skill can be invoked directly as `/implement-issue` or triggered from its description.

Official reference: https://code.claude.com/docs/en/slash-commands

## Antigravity

Workspace skills are discovered under `.agents/skills/<skill>/SKILL.md` and can be invoked as `/implement-issue`. Agent Skills replace the legacy single-file Workflow mechanism for new work.

Official references:

- https://antigravity.google/docs/skills
- https://antigravity.google/docs/migration/workflows-to-skills

## Compatibility rule

If an agent surface later changes how skills are discovered, update only the adapter/installer/docs unless the open workflow semantics themselves changed. Provider behavior must not leak into `core/`.

## Release verification

Structural adapter checks are not equivalent to live host verification. For adapter/invocation changes and periodic release confidence, use the disposable smoke procedure in [compatibility-release.md](compatibility-release.md).
