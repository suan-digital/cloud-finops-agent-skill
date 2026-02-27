# Changelog

All notable changes to the Cloud FinOps Agent Skill will be documented in this file.

## [1.0.0] — 2026-02-27

### Added

- **SKILL.md** — Primary entry point with 6-step reasoning sequence, two-tier routing (business problem → provider/technology), 8 analysis dimensions, and quality standards

#### Methodology References
- **suan-methodology.md** — 5 advisory principles: cost is architecture, maturity is a journey, diagnose before prescribing, quick wins build trust, every optimization has a carbon dividend
- **intake-protocol.md** — Structured questionnaire (6 categories, 40+ questions) with file analysis routing
- **output-format.md** — 9-section report template with examples and formatting guidelines
- **file-analysis.md** — Analysis protocols for Terraform, Kubernetes manifests, cloud bills, and architecture documents
- **adaptation-patterns.md** — Adaptation by spend tier (startup/mid-market/enterprise), AI maturity (none/experiment/production/heavy), and engagement type

#### Framework & Maturity References
- **shuhari-maturity.md** — 守破離 maturity model with assessment framework, readiness checklists, and anti-patterns for each stage
- **architecture-cost.md** — "80% locked at design time" with architectural cost traps, shift-left visibility, unit economics, and engineering ownership model
- **finops-framework.md** — Full FinOps Foundation framework: 6 principles, 3 phases, 4 domains, 22 capabilities with Crawl/Walk/Run matrices, FOCUS specification, and FinOps for AI

#### AI-Specific References
- **ai-cost-visibility.md** — 4-5x hidden cost multiplier with cost breakdown, three hidden cost patterns, and visibility maturity levels
- **inference-economics.md** — 5-lever playbook (model routing, prompt optimization, semantic caching, cost attribution, quantization) with agentic multiplier analysis
- **genai-capacity.md** — Provisioned vs. on-demand vs. spot, spillover management, GPU sizing, auto-scaling strategies, and multi-model capacity planning
- **ai-value-governance.md** — AI investment council, stage gate framework, ROI measurement, portfolio management, and organizational patterns

#### Operations References
- **greenops-playbook.md** — 8-fix remediation playbook with carbon-aware computing patterns
- **tagging-governance.md** — Tag taxonomy, enforcement mechanisms (prevention/detection/remediation), IaC integration, and coverage metrics
- **cost-visibility-tooling.md** — Tool categories (native, third-party, shift-left, AI-powered, FOCUS), anomaly detection, and tool selection decision tree

#### Cloud Provider References
- **cloud-aws.md** — CUR, Savings Plans, RIs, 50+ service-level patterns (EC2, EBS, S3, RDS, Lambda, EKS, data transfer, CloudWatch)
- **cloud-azure.md** — Cost Management, reservations, Savings Plans, Hybrid Benefit, 40+ patterns (VMs, Storage, SQL, AKS, Functions)
- **cloud-gcp.md** — Billing export, CUDs, SUDs, 25+ patterns (Compute Engine, GKE, BigQuery, Cloud Storage, Cloud SQL)
- **cloud-oci.md** — OCI billing, Universal Credits, patterns for Compute, OKE, Oracle Database, networking advantages

#### AI Provider References
- **ai-anthropic.md** — Claude pricing, prompt caching, Batch API, model routing, extended thinking optimization
- **ai-bedrock.md** — Bedrock pricing models, provisioned throughput, Model Units, spillover management, agent cost tracking
- **ai-azure-openai.md** — PTU management, spillover control, reasoning model economics, Global vs. Regional deployments
- **ai-vertex.md** — Gemini model routing, context caching, batch predictions, endpoint management, multi-modal pricing

#### Data Platform References
- **data-databricks.md** — DBU optimization, Photon evaluation, warehouse sizing, Unity Catalog, Jobs vs. All-Purpose compute
- **data-snowflake.md** — Credit optimization, warehouse sizing, auto-suspend tuning, query cost optimization, Cortex AI

#### Packaging
- **install.sh** — One-liner installer script
- **README.md** — Project overview and quick start
- **INSTALLATION.md** — 5 installation methods
- **LICENSE.md** — CC BY-SA 4.0
- **CHANGELOG.md** — This file
- **.github/CONTRIBUTING.md** — Contribution guidelines
