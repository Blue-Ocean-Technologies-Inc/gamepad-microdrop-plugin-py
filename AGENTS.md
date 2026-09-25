# AGENTS.md — Gamepad MicroDrop plugin

Code style, import ordering, Traits typing, and the pub/sub conventions are
Microdrop's: read `AGENTS.md` and `docs/CLAUDE.md` in
https://github.com/Blue-Ocean-Technologies-Inc/Microdrop before writing code
here. This file covers what is specific to this plugin.

## Packages

- `gamepad_controls`

This plugin is frontend-only (no backend group). Packages never import each
other directly (enforced by `.importlinter`); from Microdrop plugins only
`consts` modules are imported.

## Environment and tests

This repo is not a pixi workspace. Clone it under
`pixi-microdrop/microdrop-py/` and use that workspace's `test` environment,
which has Microdrop's `src` on the path and no released copy of this plugin:

    pixi run --manifest-path ../pyproject.toml -e test python -m pytest -q

CI runs the pure-unit tests the same way on every PR (`unit-tests.yml`).

## Hooks and releases

`pixi run setup-hooks` (from `pixi-microdrop/microdrop-py`) installs the
pre-commit hooks: Conventional Commits, ruff, copyright header, import-section
headers, import-linter. Every push to `main` with a `feat`/`fix`/`refactor`/
`perf` commit publishes a new version to `prefix.dev/microdrop-plugins`;
other commit types do not release.
