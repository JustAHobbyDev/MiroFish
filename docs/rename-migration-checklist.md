# Rename Migration Checklist

Date: March 19, 2026

## Goal

Execute a future rename and rebrand as one deliberate migration instead of many
partial edits.

## Phase 1: Decide Identity

- Final project name
- One-sentence product description
- Attribution language for upstream origin
- Whether simulation remains part of the top-level product framing

## Phase 2: User-Facing Rename

- Repository name
- README title and overview
- README-EN title and overview
- Frontend visible product name
- Browser title and landing copy
- Demo references and screenshots if they imply the old identity

## Phase 3: Developer-Facing Rename

- Root `package.json` name and description
- Backend project metadata in `backend/pyproject.toml`
- Docker labels or image names
- CI or release metadata
- Any scripts that expose user-facing names

## Phase 4: Docs Cleanup

- Replace fork-centered language with product-centered language
- Move upstream notes into attribution or maintenance sections
- Update architecture docs to use the current domain vocabulary
- Confirm quick-start instructions still match the repo after renaming

## Phase 5: Compatibility Review

- Decide which route names should remain stable
- Decide which artifact names need compatibility aliases
- Decide whether environment variables require deprecation shims
- Decide whether old names must remain searchable in docs for a transition period

## Validation Checklist

- Build passes
- Tests pass
- Main workflows still function
- Repo description and UI description match
- New contributor can explain the product without referencing upstream

## Do Not Do

- Do not rename purely internal identifiers unless they create real confusion.
- Do not combine unrelated refactors into the rename pass.
- Do not remove attribution to upstream history where it is still relevant.
