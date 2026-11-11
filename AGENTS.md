# AGENTS.md

## Repository state (verified)
- Git repo on `main` tracking `origin` (`https://github.com/BLEKERS/ExchangeIT-DeLaPena-JamesBenedict-G1`); no commits yet.
- Working tree currently contains untracked docs only: `AGENTS.md` and `DESIGN.md`.
- No `README`, manifests/lockfiles, build/test/lint/format/typecheck/codegen configs, CI workflows, or app/source entrypoints found.

## Design reference
- `DESIGN.md` documents a Binance-derived UI system (colors, typography, spacing, components, do/don'ts, responsive notes). If implementing UI, follow its tokens/components and rules (e.g. yellow `#fcd535` primary CTAs, BinanceNova/BinancePlex split, trading green/red semantics, dark vs light transactional surfaces) rather than inventing a visual style.

## Guidance
- No established build, test, or lint commands yet. Do not guess toolchains or scripts—inspect newly added config/manifests (e.g. `package.json`, `pyproject.toml`, workflows) before running commands.
- Re-check and update this file once source code or project configuration is added.
