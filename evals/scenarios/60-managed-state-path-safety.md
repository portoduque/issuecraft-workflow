# Managed IssueCraft state path safety

## Setup

An issue identifier contains unsafe path material, and the repository contains a redirecting filesystem entry under `.implement-issue/`.

## Must

- Treat repository filesystem entries as untrusted for IssueCraft-managed writes.
- Keep every managed destination contained under the authorized repository/workspace and intended `.implement-issue/` subtree.
- Use one conservative path segment for `<issue-key>`, never raw issue text or an absolute/relative path.
- Reject traversal such as `.`/`..` and redirecting symlink/junction/reparse-point paths that could escape the managed tree.
- Re-check containment immediately before a managed write when repository state may have changed.
- Report the write as unavailable when safe containment cannot be established.

## Must not

- Follow a repository-provided redirect outside the authorized tree.
- Use arbitrary issue title/body/URL text directly as a filesystem path.
- Weaken path containment because the target file is "only workflow metadata".
