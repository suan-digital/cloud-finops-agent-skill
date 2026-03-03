# CLAUDE.md — Project Instructions for Claude Code

## Repository

Cloud FinOps Agent Skill — the FinOps Foundation framework transcribed and structured for LLMs.

## Git Conventions

- **Commit email:** Always use `git -c user.email=github@suan.digital -c user.name="suan"` for commits
- **Branch naming:** `improve/<short-slug>` for auto-improvement PRs
- **Commit messages:** Conventional commits — `feat:`, `fix:`, `docs:`, `chore:`
- **PR titles:** Short, imperative, under 70 characters

## Content Style

- **Direct and confident** — Expert advisor tone, not cautious consultant
- **Specific and actionable** — "right-size instances" is vague; "migrate m5.4xlarge to m6i.xlarge" is actionable
- **Quantify impact** — Use ranges when exact numbers aren't available
- **Plain language** — Avoid jargon without explanation
- **Accurate statistics** — Cite sources. Do not fabricate numbers. Use "typically X–Y" if uncertain.

## File Structure

All skill content lives in `skills/cloud-finops/`:

- `SKILL.md` — Entry point with prompt + routing (the ONLY custom file)
- `references/capabilities/` — 18 capability files from `finopsfoundation/framework`
- `references/personas.md` — 8 personas from `finopsfoundation/framework`
- `references/focus/overview.md` — FOCUS spec v1.3 overview + glossary
- `references/focus/columns.md` — 75 FOCUS column definitions consolidated (cost_and_usage + contract_commitment)
- `references/focus/features.md` — 22 FOCUS supported features with SQL examples
- `references/playbooks/` — 6 implementation playbooks from Foundation working groups
- `references/kpis/` — KPI definitions, waste sensors, reduction opportunities, container labels

**Reference files are auto-generated** from `.upstream/` submodules by
`scripts/transform-upstream.py`. Never edit reference files directly — edit the
transform script instead, then regenerate.

Upstream submodules (source of truth):

- `.upstream/framework/` — `finopsfoundation/framework` (capabilities, personas)
- `.upstream/focus-spec/` — `FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec` (pinned to v1.3 tag)
- `.upstream/kpis/` — `finopsfoundation/kpis` (KPI definitions, waste sensors)

Scripts:

- `scripts/transform-upstream.py` — Reads `.upstream/`, writes `references/`. Use `--check` to verify committed files match.
- `scripts/check-submodule-freshness.py` — Compares pinned submodule commits vs remote HEAD. Use `--fetch` to pull latest.

## When Making Changes

- Read the target file(s) before editing
- Preserve existing structure and formatting conventions
- Keep tables aligned and consistent
- Do not add provider vendor recommendations unless backed by data
- Statistics must come from reference files or well-known industry sources
