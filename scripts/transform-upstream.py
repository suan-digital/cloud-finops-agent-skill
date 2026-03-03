#!/usr/bin/env python3
"""Transform upstream submodule content into LLM-optimized reference files.

Reads from .upstream/ git submodules and writes to skills/cloud-finops/references/.
Generated files are committed — the skill works on git clone without a build step.

Usage:
  python scripts/transform-upstream.py           # regenerate all reference files
  python scripts/transform-upstream.py --check   # verify committed files match (CI)

Exit codes:
  0 — success (files written, or --check passes)
  1 — --check failed (committed files differ from generated)
"""

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM = REPO_ROOT / ".upstream"
REFERENCES = REPO_ROOT / "skills" / "cloud-finops" / "references"

FRAMEWORK_DIR = UPSTREAM / "framework"
FOCUS_DIR = UPSTREAM / "focus-spec"
KPIS_DIR = UPSTREAM / "kpis"


def strip_front_matter(text):
    """Remove YAML front matter delimited by --- ... --- from markdown."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            # Skip past the closing --- and the newline after it
            return text[end + 4:].lstrip("\n")
    return text


def replace_jekyll_includes(text):
    """Replace Jekyll/Liquid {% include ... %} tags with placeholder text."""
    text = re.sub(
        r'^[ \t]*\{%\s*include\s+\S+\s*%\}[ \t]*$',
        '[See finops.org for full content]',
        text,
        flags=re.MULTILINE,
    )
    return text


def strip_html_comments(text):
    """Remove HTML comments like <!-- ... -->."""
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    return text


def strip_skip_toc(text):
    """Remove <!--SkipTOC--> markers from headings."""
    return text.replace("<!--SkipTOC-->", "")


def strip_internal_links(text):
    """Convert [text](#anchor) markdown links to just text."""
    return re.sub(r'\[([^\]]+)\]\(#[^)]+\)', r'\1', text)


def strip_glossary_links(text):
    """Convert [*term*](#glossary:term) to just *term*."""
    text = re.sub(r'\[\*([^*]+)\*\]\(#glossary:[^)]+\)', r'*\1*', text)
    # Also handle non-italic glossary links: [term](#glossary:term) → term
    text = re.sub(r'\[([^\]]+)\]\(#glossary:[^)]+\)', r'\1', text)
    return text


def strip_reference_links(text):
    """Convert [text][REF] reference-style links to just text."""
    text = re.sub(r'\[([^\]]+)\]\[[A-Z]+\]', r'\1', text)
    return text


def strip_html_anchors(text):
    """Convert <a name="..."><b>Term</b></a> to just **Term**."""
    text = re.sub(
        r'<a\s+name="[^"]*"><b>([^<]+)</b></a>',
        r'**\1**',
        text,
    )
    return text


def convert_html_heading_divs(text):
    """Convert <div class='h4-nonindex'>Title</div> to #### Title."""
    text = re.sub(
        r"<div\s+class=['\"]h4-nonindex['\"]>([^<]+)</div>",
        r'#### \1',
        text,
    )
    return text


def strip_stub_sections(text):
    """Remove placeholder stubs left by Jekyll include replacements.

    Removes:
    1. Sections where the only content is [See finops.org for full content]
       (with optional italic boilerplate description)
    2. Standalone placeholder lines after real content
    """
    # Remove sections where only content is the placeholder (optional italic line)
    text = re.sub(
        r'\n##+ [^\n]+\n(?:_[^\n]+_\n)?\n+\[See finops\.org for full content\]\n',
        '\n',
        text,
    )
    # Remove remaining standalone placeholder lines
    text = re.sub(
        r'^\[See finops\.org for full content\]\n',
        '',
        text,
        flags=re.MULTILINE,
    )
    return text


def strip_html_tags(text):
    """Remove all HTML tags (block and inline) from text."""
    return re.sub(r'<[^>]+>', '', text)


def strip_liquid_tags(text):
    """Remove Liquid/Jekyll template tags like {% ... %} and {{ ... }}."""
    text = re.sub(r'\{%.*?%\}', '', text)
    text = re.sub(r'\{\{.*?\}\}', '', text)
    return text


def clean_blank_lines(text):
    """Collapse 3+ consecutive blank lines to 2, strip trailing whitespace."""
    # Strip trailing whitespace from each line
    lines = [line.rstrip() for line in text.split('\n')]
    text = '\n'.join(lines)
    # Collapse excessive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Ensure single trailing newline
    return text.strip() + '\n'


def clean_focus(text):
    """Apply all FOCUS-specific cleaning to a text block."""
    text = strip_glossary_links(text)
    text = strip_internal_links(text)
    text = strip_reference_links(text)
    text = strip_html_anchors(text)
    text = convert_html_heading_divs(text)
    text = strip_skip_toc(text)
    return text


# ---------------------------------------------------------------------------
# Transform: Capabilities
# ---------------------------------------------------------------------------

def transform_capabilities():
    """Transform framework capability markdown files."""
    src_dir = FRAMEWORK_DIR / "_capabilities"
    dst_dir = REFERENCES / "capabilities"
    dst_dir.mkdir(parents=True, exist_ok=True)

    files = {}
    for src_path in sorted(src_dir.glob("*.md")):
        content = src_path.read_text(encoding="utf-8")

        # Extract title from front matter before stripping
        title = src_path.stem  # fallback
        fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if fm_match:
            try:
                fm = yaml.safe_load(fm_match.group(1))
                title = fm.get("framework-capability-title", title)
            except yaml.YAMLError:
                pass

        content = strip_front_matter(content)
        content = replace_jekyll_includes(content)
        content = strip_html_comments(content)
        content = strip_internal_links(content)
        content = strip_glossary_links(content)
        content = strip_stub_sections(content)

        # Add source comment
        header = "<!-- Source: finopsfoundation/framework (CC BY 4.0) -->\n\n"
        content = header + content
        content = clean_blank_lines(content)

        dst_path = dst_dir / src_path.name
        files[dst_path] = content

    return files


# ---------------------------------------------------------------------------
# Transform: Personas
# ---------------------------------------------------------------------------

def transform_personas():
    """Transform personas YAML into markdown."""
    src_path = FRAMEWORK_DIR / "_data" / "personas.yml"
    dst_path = REFERENCES / "personas.md"

    personas = yaml.safe_load(src_path.read_text(encoding="utf-8"))

    lines = [
        "<!-- Source: finopsfoundation/framework/_data/personas.yml (CC BY 4.0) -->",
        "",
        "# FinOps Personas",
    ]

    for i, p in enumerate(personas):
        lines.append("")
        lines.append(f"## {p['name']}")
        lines.append("")

        if p.get("primary-goal"):
            lines.append(f"**Primary Goal:** {p['primary-goal']}")

        for section, label in [
            ("objectives", "Objectives"),
            ("frustrations", "Frustrations"),
            ("key-metrics", "Key Metrics"),
            ("finops-benefits", "FinOps Benefits"),
        ]:
            items = p.get(section, [])
            if items:
                lines.append("")
                lines.append(f"**{label}:**")
                for item in items:
                    text = item["item"] if isinstance(item, dict) else item
                    lines.append(f"- {text}")

        # Add separator between personas (not after the last one)
        if i < len(personas) - 1:
            lines.append("")
            lines.append("---")

    content = "\n".join(lines) + "\n"
    return {dst_path: content}


# ---------------------------------------------------------------------------
# Transform: FOCUS Spec
# ---------------------------------------------------------------------------

def transform_focus():
    """Transform FOCUS spec into overview reference file.

    Assembles overview.md + cost_and_usage/dataset.md + glossary.md into a
    single LLM-optimized reference file.
    """
    spec_dir = FOCUS_DIR / "specification"
    dst_dir = REFERENCES / "focus"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst_path = dst_dir / "overview.md"

    parts = []

    # Part 1: Overview / Introduction
    overview_path = spec_dir / "overview.md"
    if overview_path.exists():
        overview = clean_focus(overview_path.read_text(encoding="utf-8"))
        parts.append(overview.strip())

    # Part 2: Supported features overview (if exists)
    sf_overview = spec_dir / "supported_features" / "supported_features_overview.md"
    if sf_overview.exists():
        sf_content = clean_focus(sf_overview.read_text(encoding="utf-8"))
        parts.append(sf_content.strip())

    # Part 3: Cost and Usage dataset summary
    dataset_path = spec_dir / "datasets" / "cost_and_usage" / "dataset.md"
    if dataset_path.exists():
        dataset = clean_focus(dataset_path.read_text(encoding="utf-8"))
        parts.append(dataset.strip())

    # Part 4: Glossary
    glossary_path = spec_dir / "glossary.md"
    if glossary_path.exists():
        glossary = clean_focus(glossary_path.read_text(encoding="utf-8"))
        parts.append(glossary.strip())

    header = "<!-- Source: FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec (Community Specification License 1.0) -->\n\n"

    # Remove page break divs
    content = header + "\n\n---\n\n".join(parts) + "\n"
    content = re.sub(r'<div style="page-break-after:\s*always"></div>\n?', '', content)
    # Remove markdown-pp directives
    content = re.sub(r'^!INCLUDE\s+.*$\n?', '', content, flags=re.MULTILINE)
    content = re.sub(r'^!TOC\s+.*$\n?', '', content, flags=re.MULTILINE)
    # Remove link reference definitions like [FODO]: https://...
    content = re.sub(r'^\[[\w-]+\]:\s+https?://.*$\n?', '', content, flags=re.MULTILINE)

    content = clean_blank_lines(content)

    return {dst_path: content}


# ---------------------------------------------------------------------------
# Transform: KPIs
# ---------------------------------------------------------------------------

def transform_kpis():
    """Transform KPIs repo content into reference files."""
    dst_dir = REFERENCES / "kpis"
    dst_dir.mkdir(parents=True, exist_ok=True)

    files = {}

    # KPI definitions from README
    kpi_readme = KPIS_DIR / "README.md"
    if kpi_readme.exists():
        content = kpi_readme.read_text(encoding="utf-8")
        # Strip license badge block at the top
        content = re.sub(
            r'^Shield:.*?\n\n',
            '',
            content,
            count=1,
            flags=re.DOTALL,
        )
        # Strip license text paragraph
        content = re.sub(
            r'^This work is licensed under.*?\n\n.*?\n\n.*?\n\n',
            '',
            content,
            count=1,
            flags=re.DOTALL,
        )
        # Replace repo heading with our heading
        content = re.sub(r'^# kpis\b', '# FinOps KPIs', content, flags=re.MULTILINE)
        # Normalize list markers (* → -) for consistency with our style
        content = re.sub(r'^\* ', '- ', content, flags=re.MULTILINE)

        header = "<!-- Source: finopsfoundation/kpis (CC BY-SA 4.0) -->\n\n"
        content = header + content
        content = clean_blank_lines(content)
        files[dst_dir / "kpi-definitions.md"] = content

    # Waste sensors from YAML
    ws_yaml = KPIS_DIR / "waste-sensors" / "waste-sensors.yml"
    ws_readme = KPIS_DIR / "waste-sensors" / "README.md"
    if ws_yaml.exists() and ws_readme.exists():
        # Parse the multi-document YAML (--- separated)
        sensors = list(yaml.safe_load_all(ws_yaml.read_text(encoding="utf-8")))

        # Build from waste-sensors README (methodology) + YAML data (table)
        readme_content = ws_readme.read_text(encoding="utf-8")

        lines = [
            "<!-- Source: finopsfoundation/kpis/waste-sensors (CC BY-SA 4.0) -->",
            "",
            "# Waste Sensors",
            "",
            "Waste sensors are standardized definitions for potential unrealized savings opportunities.",
            "Tools implement their own visualization and remediation code and use the *id* key to get",
            "descriptions from the FinOps Foundation repository. This standardizes terms across the FinOps domain.",
            "",
            "## Waste KPIs",
            "",
            "Each waste sensor aggregates a type of unrealized savings opportunities into two types of KPIs:",
            "- **Savings Opportunity** — the actual amount of cost reduction (not the total cost of the unoptimized workload)",
            "- **Waste Percentage** — how much of a workload is in an unoptimized state",
            "",
            "When listing multiple waste sensors, sort by largest savings opportunity first.",
            "",
            "### Savings Opportunity Example",
            "",
            "If total EC2 spend in an account is $1,000 and $200 has low utilization and can be sized",
            "one size smaller, the savings opportunity is $100 (the $200 reduced by half). The waste",
            "percentage is $100 / $1,000 = 10%.",
            "",
            "## Waste Goals",
            "",
            "A good starting point is to target a Waste Percentage of 5% or less for all workloads.",
            "Goals can be customized by tags (account, application, business unit, etc.).",
            "Performance toward goals should be tracked over time (e.g., monthly Waste Percentage",
            "over 12 months graphed against the target).",
            "",
            "## Waste Exceptions",
            "",
            "Occasionally workloads may need temporary exceptions from waste sensor tracking",
            "(e.g., Cassandra clusters that cannot easily auto-scale). Exceptions should be",
            "tracked separately with expiration dates.",
            "",
            "## Sensor Definitions",
            "",
            "| ID | Display Name | Provider | Description | Comment |",
            "|---|---|---|---|---|",
        ]

        for sensor in sensors:
            if sensor is None:
                continue
            sid = sensor.get("id", "")
            name = sensor.get("display_name", "")
            provider = sensor.get("cloud_provider", "")
            desc = sensor.get("description", "")
            comment = sensor.get("comment", "")
            lines.append(f"| `{sid}` | {name} | {provider} | {desc} | {comment} |")

        content = "\n".join(lines) + "\n"
        files[dst_dir / "waste-sensors.md"] = content

    return files


# ---------------------------------------------------------------------------
# Transform: FOCUS Columns (Phase 1)
# ---------------------------------------------------------------------------

def transform_focus_columns():
    """Consolidate all FOCUS column definitions into a single reference file.

    Reads individual column specs from cost_and_usage and contract_commitment
    datasets, extracts key fields, and produces one combined markdown file.
    """
    dst_dir = REFERENCES / "focus"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst_path = dst_dir / "columns.md"

    datasets = [
        (
            "Cost and Usage Columns",
            FOCUS_DIR / "specification" / "datasets" / "cost_and_usage" / "columns",
        ),
        (
            "Contract Commitment Columns",
            FOCUS_DIR / "specification" / "datasets" / "contract_commitment" / "columns",
        ),
    ]

    all_sections = []

    for heading, col_dir in datasets:
        if not col_dir.exists():
            continue

        sections = []
        for col_path in sorted(col_dir.glob("*.md")):
            # Skip .mdpp template files
            if col_path.suffix != ".md" or ".mdpp" in col_path.name:
                continue

            raw = col_path.read_text(encoding="utf-8")
            text = clean_focus(raw)

            sections.append(text.strip())

        if sections:
            all_sections.append(f"# {heading}\n\n" + "\n\n---\n\n".join(sections))

    header = "<!-- Source: FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec (Community Specification License 1.0) -->\n\n"
    content = header + "\n\n---\n\n".join(all_sections) + "\n"

    # Remove page-break divs, markdown-pp directives, link reference definitions
    content = re.sub(r'<div style="page-break-after:\s*always"></div>\n?', '', content)
    content = re.sub(r'^!INCLUDE\s+.*$\n?', '', content, flags=re.MULTILINE)
    content = re.sub(r'^!TOC\s+.*$\n?', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\[[\w-]+\]:\s+https?://.*$\n?', '', content, flags=re.MULTILINE)

    content = clean_blank_lines(content)
    return {dst_path: content}


# ---------------------------------------------------------------------------
# Transform: FOCUS Features (Phase 1)
# ---------------------------------------------------------------------------

def transform_focus_features():
    """Consolidate FOCUS supported feature guides into a single reference file.

    Preserves descriptions, dependent/supporting columns, and SQL examples.
    Skips the overview file (already included in focus/overview.md).
    """
    dst_dir = REFERENCES / "focus"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst_path = dst_dir / "features.md"

    src_dir = FOCUS_DIR / "specification" / "supported_features"
    if not src_dir.exists():
        return {}

    sections = []
    for feat_path in sorted(src_dir.glob("*.md")):
        # Skip .mdpp files and the overview (already in overview.md)
        if ".mdpp" in feat_path.name:
            continue
        if feat_path.name == "supported_features_overview.md":
            continue

        raw = feat_path.read_text(encoding="utf-8")
        text = clean_focus(raw)

        sections.append(text.strip())

    header = "<!-- Source: FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec (Community Specification License 1.0) -->\n\n"
    content = header + "\n\n---\n\n".join(sections) + "\n"

    # Same cleanup as overview
    content = re.sub(r'<div style="page-break-after:\s*always"></div>\n?', '', content)
    content = re.sub(r'^!INCLUDE\s+.*$\n?', '', content, flags=re.MULTILINE)
    content = re.sub(r'^!TOC\s+.*$\n?', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\[[\w-]+\]:\s+https?://.*$\n?', '', content, flags=re.MULTILINE)

    content = clean_blank_lines(content)
    return {dst_path: content}


# ---------------------------------------------------------------------------
# Transform: Playbooks (Phase 2)
# ---------------------------------------------------------------------------

# Curated list of 6 highest-impact playbooks (not all 17).
PLAYBOOK_SOURCES = [
    ("forecasting", "project--forecasting-playbook.md"),
    ("container-costs", "project--container-costs.md"),
    ("shared-costs", "project--shared-costs.md"),
    ("unit-economics", "project--unit-economics.md"),
    ("engineers-action", "project--engineers-action.md"),
    ("adopting-finops", "project--adopting-finops.md"),
]


def transform_playbooks():
    """Transform Foundation playbook markdown files into reference files.

    Strips Jekyll front matter, HTML, Liquid tags, and internal links.
    Each playbook becomes a separate file under references/playbooks/.
    """
    src_dir = FRAMEWORK_DIR / "_resources"
    dst_dir = REFERENCES / "playbooks"
    dst_dir.mkdir(parents=True, exist_ok=True)

    files = {}
    for slug, filename in PLAYBOOK_SOURCES:
        src_path = src_dir / filename
        if not src_path.exists():
            print(f"  WARNING: playbook not found: {src_path}")
            continue

        content = src_path.read_text(encoding="utf-8")

        content = strip_front_matter(content)
        content = strip_html_comments(content)
        content = strip_html_tags(content)
        content = strip_liquid_tags(content)
        content = replace_jekyll_includes(content)
        content = strip_internal_links(content)
        content = strip_glossary_links(content)

        # Strip site-relative links like [text](/framework/...) → text
        content = re.sub(r'\[([^\]]+)\]\(/[^)]+\)', r'\1', content)

        header = f"<!-- Source: finopsfoundation/framework/_resources/{filename} (CC BY 4.0) -->\n\n"
        content = header + content
        content = clean_blank_lines(content)

        dst_path = dst_dir / f"{slug}.md"
        files[dst_path] = content

    return files


# ---------------------------------------------------------------------------
# Transform: Reducing Waste YAML (Phase 3)
# ---------------------------------------------------------------------------

def transform_reducing_waste():
    """Transform reducing-waste.yml into a markdown reference table."""
    src_path = FRAMEWORK_DIR / "_data" / "reducing-waste.yml"
    dst_dir = REFERENCES / "kpis"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst_path = dst_dir / "reducing-waste.md"

    if not src_path.exists():
        return {}

    entries = yaml.safe_load(src_path.read_text(encoding="utf-8"))
    if not entries:
        return {}

    lines = [
        "<!-- Source: finopsfoundation/framework/_data/reducing-waste.yml (CC BY 4.0) -->",
        "",
        "# Cloud Waste Reduction Opportunities",
        "",
        "Specific optimization opportunities by cloud provider and service, curated by the",
        "FinOps Foundation Reducing Waste working group. Savings potential: $ = low,",
        "$$ = medium, $$$ = high.",
        "",
        "| Cloud Provider | Product | Service | Type | Savings | Description |",
        "|---|---|---|---|---|---|",
    ]

    for entry in entries:
        if entry is None:
            continue
        provider = entry.get("cloud-provider", "")
        product = entry.get("cloud-product", "")
        service = entry.get("cloud-service-name", "")
        etype = entry.get("type", "")
        savings = entry.get("savings-potential", "")
        if savings is None:
            savings = ""
        desc = entry.get("description", "")
        # Escape pipes in description for table safety
        desc = str(desc).replace("|", "\\|") if desc else ""
        lines.append(f"| {provider} | {product} | {service} | {etype} | {savings} | {desc} |")

    content = "\n".join(lines) + "\n"
    return {dst_path: content}


# ---------------------------------------------------------------------------
# Transform: Container Cost Allocation Labels (Phase 3)
# ---------------------------------------------------------------------------

def transform_container_labels():
    """Transform container-cost-allocation.yml into structured markdown."""
    src_path = FRAMEWORK_DIR / "_data" / "container-cost-allocation.yml"
    dst_dir = REFERENCES / "kpis"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst_path = dst_dir / "container-labels.md"

    if not src_path.exists():
        return {}

    labels = yaml.safe_load(src_path.read_text(encoding="utf-8"))
    if not labels:
        return {}

    lines = [
        "<!-- Source: finopsfoundation/framework/_data/container-cost-allocation.yml (CC BY 4.0) -->",
        "",
        "# Container Cost Allocation Labels",
        "",
        "Kubernetes label strategies for container cost allocation, curated by the FinOps Foundation",
        "Containers SIG. Labels are organized by maturity level (Crawl/Walk/Run) and mapped to personas.",
        "",
    ]

    for label in labels:
        if label is None:
            continue
        name = label.get("label-name", "")
        # Skip call-for-contribution placeholder entries
        if name == "call-for-contribution":
            continue

        definition = label.get("label-definition", "")
        context = label.get("context", "")
        resources = label.get("common-resources", "")
        aliases = label.get("label-alias", "")
        example = label.get("example", "")
        personas = label.get("personas", [])
        maturity = label.get("maturity", "")

        lines.append(f"## `{name}`")
        lines.append("")
        if definition:
            lines.append(definition)
            lines.append("")
        lines.append(f"- **Context:** {context}")
        lines.append(f"- **Maturity:** {maturity.title() if maturity else ''}")
        lines.append(f"- **Common Resources:** {resources}")
        if aliases:
            lines.append(f"- **Aliases:** {aliases}")
        if example:
            lines.append(f"- **Example:** {example}")
        if personas:
            persona_str = ", ".join(p.title() if isinstance(p, str) else str(p) for p in personas)
            lines.append(f"- **Personas:** {persona_str}")
        lines.append("")

    content = "\n".join(lines)
    content = clean_blank_lines(content)
    return {dst_path: content}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def validate_submodules():
    """Check that all required submodules are present."""
    missing = []
    for name, path in [("framework", FRAMEWORK_DIR), ("focus-spec", FOCUS_DIR), ("kpis", KPIS_DIR)]:
        if not path.exists() or not any(path.iterdir()):
            missing.append(name)
    if missing:
        print(f"ERROR: Missing submodules: {', '.join(missing)}")
        print("Run: git submodule update --init")
        sys.exit(1)


def main():
    check_mode = "--check" in sys.argv
    validate_submodules()

    print("Transforming upstream content...")
    all_files = {}
    all_files.update(transform_capabilities())
    all_files.update(transform_personas())
    all_files.update(transform_focus())
    all_files.update(transform_focus_columns())
    all_files.update(transform_focus_features())
    all_files.update(transform_kpis())
    all_files.update(transform_playbooks())
    all_files.update(transform_reducing_waste())
    all_files.update(transform_container_labels())

    if check_mode:
        mismatches = []
        for path, expected in sorted(all_files.items()):
            if not path.exists():
                mismatches.append(f"  MISSING: {path.relative_to(REPO_ROOT)}")
            else:
                actual = path.read_text(encoding="utf-8")
                if actual != expected:
                    mismatches.append(f"  DIFFERS: {path.relative_to(REPO_ROOT)}")

        if mismatches:
            print(f"\n## Transform Check FAILED ({len(mismatches)} file(s))\n")
            for m in mismatches:
                print(m)
            print("\nRun `python scripts/transform-upstream.py` to regenerate.")
            sys.exit(1)
        else:
            print(f"All {len(all_files)} reference files match transform output.")
            sys.exit(0)
    else:
        for path, content in sorted(all_files.items()):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            print(f"  wrote {path.relative_to(REPO_ROOT)}")

        print(f"\nDone — {len(all_files)} files written.")


if __name__ == "__main__":
    main()
