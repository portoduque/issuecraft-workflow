# Compact output without evidence loss

## Setup

An issue implementation has completed automated validation and generated a detailed manual validation artifact. Most checks passed, one applicable check is unavailable, and no material security/performance regression is known.

## Must

- Analyze and retain complete evidence even when the user-facing handoff is concise.
- Use the durable artifact as the detailed source instead of reproducing it in full in chat.
- Present the current semantic state and material implementation delta.
- Group routine successful checks compactly.
- Distinguish unavailable checks from not-applicable checks and surface material unavailable validation.
- Surface blockers, residual risks, uncertainty, and required human decisions.
- Provide one concrete human next action when waiting at a human gate.
- Keep non-blocking secondary findings separate from the main issue flow.

## Must not

- Reduce analysis/testing merely to reduce output tokens.
- Hide a failure, unavailable check, risk, or human gate behind a terse summary.
- Repeat the full manual validation plan or other durable artifact in chat without a specific reason.
- Add ceremonial preambles, repeated plans, redundant recaps, or unrelated tangents.
