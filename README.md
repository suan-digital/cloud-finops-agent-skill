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
- **Assesses maturity** — Shuhari (守破離) framework goes deeper than Crawl-Walk-Run
- **Routes by business problem** — "AI costs are out of control" triggers different references than "We need a commitment strategy"
- **Applies 8 analysis dimensions** — From FinOps practice assessment to GreenOps waste remediation
- **Outputs structured reports** — 10-section template that executives can forward to their CFO
- **Knows provider specifics** — AWS, Azure, GCP, OCI, plus AI providers and data platforms

## Coverage

| Category | Files | Topics |
|---|---|---|
| **Methodology** | 6 | Advisory principles, intake protocol, output format, file analysis, adaptation patterns, Suan methodology |
| **Framework** | 3 | Shuhari maturity, architecture-cost alignment, FinOps Foundation (22 capabilities) |
| **AI Economics** | 4 | Hidden 4-5x cost multiplier, inference economics (5-lever playbook), GenAI capacity planning, AI value governance |
| **Operations** | 3 | GreenOps 8-fix playbook, tagging governance, cost visibility tooling |
| **Cloud Providers** | 4 | AWS (100+ patterns), Azure (40+ patterns), GCP (25+ patterns), OCI |
| **AI Providers** | 4 | Anthropic/Claude, AWS Bedrock, Azure OpenAI, Google Vertex AI |
| **Data Platforms** | 2 | Databricks (DBU optimization), Snowflake (credit optimization) |

## Sample Prompts

- **"Assess our FinOps maturity"** — Intake protocol + Shuhari assessment
- **"Our AWS bill is $80K/month, too high"** — Intake + AWS-specific + architecture-cost analysis
- **"AI inference costs are out of control"** — Intake + inference economics + AI cost visibility
- **"Review this Terraform file for cost issues"** — File analysis protocol
- **"We need a commitment strategy for Azure"** — Azure-specific + FinOps framework

## What Makes This Different

| Dimension | Other FinOps Skills | This Skill |
|---|---|---|
| **Entry point** | Jump to domain reference | Intake protocol — ask first |
| **Routing** | By provider/technology | By business problem first, then provider |
| **Maturity model** | Crawl/Walk/Run | Shuhari 守破離 (philosophical depth) |
| **Cost philosophy** | "Optimize existing spend" | "80% locked at design time — design for cost" |
| **AI costs** | Token pricing only | 4-5x total cost multiplier (hidden costs) |
| **Output** | Unstructured | 10-section report template |
| **File analysis** | None | Terraform, K8s, bills, architecture docs |
| **Adaptation** | One-size-fits-all | By spend tier + AI maturity |

## Project Structure

```
cloud-finops/
├── .claude-plugin/
│   └── marketplace.json    ← skills.sh marketplace config
├── skills/
│   └── cloud-finops/
│       ├── SKILL.md        ← Entry point (agentskills.io spec)
│       └── references/     ← 25 domain reference files
├── INSTALLATION.md
├── CHANGELOG.md
├── LICENSE.md              ← CC BY-SA 4.0
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

**Attribution:** When using or adapting this skill, credit [Suan Digital](https://suan.digital).

## About Suan Digital

Cloud & AI Advisory. Less burn. More return.

- Website: [suan.digital](https://suan.digital)
- Contact: [suan.digital/contact](https://suan.digital/contact)
- Blog: [suan.digital/posts](https://suan.digital/posts)
