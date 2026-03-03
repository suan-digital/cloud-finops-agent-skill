# Cloud FinOps Agent Skill

The FinOps Foundation framework transcribed and structured for AI agents. All reference content is sourced directly from Foundation repositories — no custom content. Installable in one command via [skills.sh](https://skills.sh).

## Quick Start

```bash
npx skills add suan-digital/cloud-finops
```

Works with Claude Code, Cursor, Codex, OpenCode, and [40+ other agents](https://skills.sh/docs/agents). See [INSTALLATION.md](INSTALLATION.md) for all methods.

## What It Does

This skill turns any AI agent into a FinOps advisor grounded in Foundation material:

- **Routes by business problem** — Condition-keyed routing loads only the capabilities needed. A targeted question loads 1-2 files, not the entire knowledge base.
- **Covers the full framework** — All domains and capabilities with Crawl/Walk/Run maturity criteria, plus all personas
- **Includes FOCUS billing spec** — Column definitions and data model for multi-cloud cost normalization
- **Waste sensor definitions** — Standardized waste sensors from the KPIs repo for identifying savings opportunities
- **Tracks upstream changes** — Submodule-based scripts detect drift in Foundation repos, FOCUS spec releases, and KPI definitions

## Source Repositories

| Repo | Content | License |
|---|---|---|
| [finopsfoundation/framework](https://github.com/finopsfoundation/framework) | Capabilities, personas, playbooks | CC BY 4.0 |
| [FOCUS_Spec](https://github.com/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec) | Billing data specification | Community Specification License 1.0 |
| [finopsfoundation/kpis](https://github.com/finopsfoundation/kpis) | KPI definitions, waste sensors | CC BY-SA 4.0 |

## Sample Prompts

- **"Assess our FinOps maturity"** — Walks through all 18 capabilities using Crawl/Walk/Run criteria
- **"Our cloud bill is too high"** — Routes to utilization-efficiency + cost-allocation capabilities
- **"How should I structure Savings Plans?"** — Routes to manage-commitment-based-discounts capability
- **"We can't attribute costs to teams"** — Routes to cost-allocation + manage-shared-cloud-costs
- **"We had a cost spike last week"** — Routes to manage-anomalies capability
- **"Need to forecast next quarter"** — Routes to forecasting + budget-management capabilities
- **"Multi-cloud cost comparison"** — Routes to FOCUS spec + data-normalization capability
- **"Identify waste in our environment"** — Routes to waste sensors + utilization-efficiency

## Project Structure

```
cloud-finops/
├── skills/cloud-finops/
│   ├── SKILL.md                              ← Prompt + routing (only custom file)
│   └── references/                           ← Auto-generated from .upstream/
│       ├── capabilities/                     ← 18 capability files
│       ├── personas.md                       ← 8 FinOps personas
│       ├── focus/
│       │   ├── overview.md                   ← FOCUS spec overview + glossary
│       │   ├── columns.md                    ← 75 column definitions
│       │   └── features.md                   ← 22 supported features
│       ├── kpis/
│       │   ├── kpi-definitions.md            ← KPI definitions
│       │   ├── waste-sensors.md              ← Standardized waste sensors
│       │   ├── reducing-waste.md             ← Waste reduction opportunities
│       │   └── container-labels.md           ← Container cost allocation labels
│       └── playbooks/                        ← 6 implementation playbooks
├── .upstream/                                ← Git submodules (source of truth)
│   ├── framework/                            ← finopsfoundation/framework
│   ├── focus-spec/                           ← FOCUS_Spec (pinned to v1.3)
│   └── kpis/                                 ← finopsfoundation/kpis
├── scripts/
│   ├── transform-upstream.py                 ← Reads .upstream/, writes references/
│   └── check-submodule-freshness.py          ← Submodule drift detection
├── .claude-plugin/marketplace.json           ← skills.sh marketplace config
├── INSTALLATION.md
├── CHANGELOG.md
└── LICENSE.md                                ← CC BY-SA 4.0
```

## Content Monitoring

Two scripts keep the skill aligned with upstream sources:

- **`transform-upstream.py`** — Reads `.upstream/` submodules and writes `references/`. Use `--check` to verify committed files match.
- **`check-submodule-freshness.py`** — Compares pinned submodule commits against remote HEAD to detect upstream drift.

## Contributing

See [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md). Contributions welcome — especially:
- Updated transcriptions when upstream repos change
- Bug fixes in monitoring scripts

## License

CC BY-SA 4.0 — See [LICENSE.md](LICENSE.md)
