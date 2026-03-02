# Cloud FinOps

**Give any AI agent FinOps expertise.** Cloud cost optimization using the FinOps Foundation framework — installable in one command via [skills.sh](https://skills.sh).

## Quick Start

```bash
npx skills add suan-digital/cloud-finops
```

Works with Claude Code, Cursor, Codex, OpenCode, and [40+ other agents](https://skills.sh/docs/agents). See [INSTALLATION.md](INSTALLATION.md) for all methods.

## What It Does

This skill turns any AI agent into a FinOps advisor that:

- **Asks before prescribing** — Structured intake gathers context before analysis
- **Assesses maturity** — Crawl-Walk-Run maturity model provides depth beyond labels
- **Routes by business problem** — "AI costs are out of control" triggers different references than "We need a commitment strategy"
- **Applies 8 analysis dimensions** — From FinOps practice assessment to sustainability & waste remediation
- **Outputs structured reports** — 10-section template that executives can forward to their CFO
- **Knows provider specifics** — AWS, Azure, GCP, OCI, plus AI providers and data platforms

## Sample Prompts

- **"Assess our FinOps maturity"** — Intake protocol + maturity assessment
- **"Our AWS bill is $80K/month, too high"** — Intake + AWS-specific + architecture-cost analysis
- **"AI inference costs are out of control"** — Intake + inference economics + AI cost visibility
- **"Review this Terraform file for cost issues"** — File analysis protocol
- **"We need a commitment strategy for Azure"** — Azure-specific + FinOps framework

## Project Structure

```
cloud-finops/
├── .claude-plugin/
│ └── marketplace.json ← skills.sh marketplace config
├── skills/
│ └── cloud-finops/
│ ├── SKILL.md ← Entry point (agentskills.io spec)
│ └── references/ ← 25 domain reference files
├── INSTALLATION.md
├── CHANGELOG.md
├── LICENSE.md ← CC BY-SA 4.0
└── .github/
 └── CONTRIBUTING.md
```

## Contributing

See [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md). Contributions welcome — especially:
- Updated pricing data
- New optimization patterns from real engagements
- Additional provider coverage

## License

CC BY-SA 4.0 — See [LICENSE.md](LICENSE.md)

**Attribution:** When using or adapting this skill, credit the original authors.
