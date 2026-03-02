# FinOps Maturity Model

The FinOps Foundation's Crawl-Walk-Run model is useful shorthand, but organizations often
treat it as a race — rushing to "Run" before the fundamentals are solid. Each stage serves a
purpose. Maturity requires patience, and "Run" means something deeper than "doing more."

## The Three Stages

### Crawl — Build the Foundation

**Duration:** 6-12 months typical. Some organizations need longer. That's not failure.

Crawl is about repetition until basics become second nature. You don't skip steps. You don't
innovate yet. You build the habits and visibility that everything else depends on.

#### What Crawl Looks Like

- Implement cost visibility across all cloud accounts
- Establish tagging standards and enforce consistently (target: 80%+ coverage)
- Create showback reports so teams see their spend
- Set up anomaly alerts for unexpected cost spikes
- Learn one provider's pricing model deeply before adding complexity
- Develop intuition through observing cost patterns daily/weekly

#### The Crawl Mistake

Organizations treat visibility as a checkbox. "We have a dashboard, let's move on."

Crawl isn't about having a dashboard. It's about developing intuition. When you've spent months
watching cost patterns, you start recognizing anomalies before alerts fire. You understand which
services drive spend. You know which teams respond to cost data and which ignore it.

This intuition can't be automated. It can't be purchased from a vendor. It comes from
repetition, observation, and patience.

#### Readiness to Leave Crawl

All of these must be true:

- [ ] You can explain your cost structure without looking at a dashboard
- [ ] Teams know their spend and can predict it reasonably well
- [ ] Anomalies get investigated, not ignored
- [ ] Tagging coverage exceeds 80%
- [ ] You understand unit economics for primary workloads
- [ ] Cost conversations happen regularly, not just at billing surprises

#### Crawl Anti-Patterns

- Buying advanced tooling before understanding what to measure
- Implementing chargeback before teams understand their spend
- Purchasing commitments (RIs/SPs) based on guesswork rather than data
- Benchmarking against organizations at different stages
- Declaring victory because a dashboard exists

### Walk — Adapt and Develop Judgment

**Duration:** 12-24 months typical. Organizations that rush through return to relearn.

Walk is when you start questioning why practices work. You study other approaches. You
experiment. You adapt methods to your own circumstances.

In FinOps, Walk means deliberately evolving beyond the rigid rules that served you in Crawl,
because you now understand why those rules existed.

#### What Walk Looks Like

- Automate repetitive optimizations
- Build chargeback models that create real accountability
- Experiment with commitment strategies (RIs, Savings Plans, CUDs)
- Integrate cost considerations into CI/CD pipelines
- Learn from other organizations' FinOps practices
- Understand the relationship between utilization, performance, and cost
- Develop judgment about when best practices don't apply

#### The Key Shift

In Crawl, you tagged resources because the policy said to. In Walk, you understand that tagging
enables allocation > allocation enables accountability > accountability changes behavior. Now
you make intelligent decisions about when tagging matters and when it doesn't.

In Crawl, you right-sized instances because a tool recommended it. In Walk, you understand the
relationship between utilization, performance, and cost, and can have nuanced conversations
with engineering about acceptable trade-offs.

#### The Walk Danger

Many organizations get stuck here. They've moved beyond rigid rules but replaced them with new
rigid rules from a different source.

They read that Company X achieved 40% savings with a particular approach, so they copy it
exactly. They attend a conference and implement whatever the speaker recommended. They hire a
consultant and follow the playbook without adaptation.

That's not Walk. That's Crawl with a different teacher.

True Walk means developing judgment — understanding principles deeply enough to know when best
practices don't apply to your situation.

#### Readiness to Leave Walk

All of these must be true:

- [ ] You can articulate why practices work for your organization and not others
- [ ] You've tried multiple approaches and understand their trade-offs
- [ ] Your automation reflects your specific needs, not generic recommendations
- [ ] You can predict how changes will affect your cost structure
- [ ] Engineering and finance speak the same language about cloud economics
- [ ] Cost optimization suggestions come from engineering teams, not just FinOps

#### Walk Anti-Patterns

- Copying another organization's FinOps playbook exactly
- Automating without understanding what you're automating
- Treating all workloads the same (one-size-fits-all commitment strategy)
- Over-investing in tooling while under-investing in organizational change
- Confusing tool sophistication with organizational maturity

### Run — Internalize and Transcend

**Duration:** Rare. Not the goal for every capability.

Run is mastery. The organization operates in ways no playbook prescribed, yet every decision
reflects deep understanding of fundamentals.

In FinOps, Run means the framework is no longer needed because the principles are internalized.

#### What Run Looks Like

- Cost optimization is embedded in how the organization builds, not applied after
- Teams self-govern without central enforcement
- Practices evolve organically based on results
- The distinction between "FinOps" and "how we build things" disappears
- The organization creates approaches others study

#### Run in Practice

What does Run actually look like day-to-day?

- **Cost efficiency is embedded in sprint planning, not separate reviews.** Engineers estimate
  cost impact alongside story points. "How much will this cost to run?" is as natural a question
  as "how long will this take to build?"
- **Engineers propose cost-aware architectures without being asked.** The design doc includes
  a cost section not because a template requires it, but because the engineer considers cost
  a design constraint like latency or availability.
- **New services launch with cost dashboards on day one.** Observability includes cost from
  the start — not bolted on after the first billing surprise.
- **The FinOps team role evolves into platform engineering.** The central FinOps function
  dissolves because cost awareness is now a platform capability — built into templates,
  defaults, and guardrails that make the efficient path the easy path.
- **Cost anomalies are investigated like production incidents.** Not because policy demands it,
  but because the team instinctively treats unexpected cost as a signal that something is wrong.

#### The Paradox of Run

You can't aim for Run directly. You can't skip Crawl and Walk to get there faster. Run emerges
from fully experiencing the previous stages.

Organizations that claim Run maturity often reveal, under scrutiny, that they're performing
Walk activities with Run vocabulary. Sophisticated tooling but shallow understanding. Automated
processes they don't fully grasp.

True Run is rare. And that's fine.

#### Run Indicators

- Cost efficiency is simply part of how the organization operates, like security or reliability
- No one talks about "FinOps maturity" anymore — it's assumed
- Cost-aware decisions happen instinctively at all levels
- The organization generates novel approaches that others adopt
- FinOps practitioners move to other roles because the practice sustains itself

#### Run Anti-Patterns

Not everything that looks like Run is Run. Watch for:

- **Declaring Run because leadership stopped asking about costs.** They may have given up, not
  transcended. If cost conversations disappeared because nobody cares — that's regression, not
  mastery.
- **Sophisticated automation that nobody understands.** If the team can't explain what their
  cost automation does or why, they've built fragile complexity, not internalized practice.
  Run means understanding is deep, not that tooling is complex.
- **"We don't need FinOps" as avoidance, not mastery.** True Run organizations don't need the
  framework because they've internalized its principles. Organizations in denial don't need
  the framework because they've never engaged with it. The outputs look identical on the
  surface but the underlying reality is opposite.
- **Optimizing everything to the floor.** Run includes the wisdom to know when cost isn't the
  right constraint. Over-optimization that sacrifices velocity or reliability is Walk behavior —
  applying rules rigidly — not Run.

## Assessment Framework

### Conducting the Assessment

Map the organization against three dimensions:

**1. Overall Stage:**
- Where does the organization primarily operate? (Crawl / early Walk / mid Walk / late Walk / Run)
- What's the evidence? (List 3-5 supporting observations)

**2. Capability Variation:**
Not all capabilities are at the same stage. Map key capabilities:

| Capability | Stage | Evidence |
|---|---|---|
| Cost visibility | Walk | Dashboards automated, teams review weekly |
| Tagging governance | Crawl | Standards exist but only 60% coverage |
| Commitment strategy | Walk | SP portfolio managed, 85% utilization |
| CI/CD cost integration | Crawl | No cost gates in pipeline |
| Unit economics | Not started | No cost-per-user tracking |

**3. Advancement Readiness:**
- Which stage-exit criteria are met?
- Which are gaps?
- What's the recommended next milestone?

### Quick Scoring

Rate each area 1-5 and sum for overall positioning:

| Area | 1 (Crawl) | 3 (Walk) | 5 (Run) |
|---|---|---|---|
| Cost visibility | Manual exports | Automated dashboards | Self-service, real-time |
| Accountability | Central team only | Showback to teams | Teams self-govern |
| Optimization | Reactive | Scheduled reviews | Continuous, automated |
| Architecture | Cost as afterthought | Cost in reviews | Cost as design constraint |
| Culture | "Finance's problem" | Shared responsibility | Engineering-owned |

**Total: 5-10 = Crawl, 11-18 = Walk, 19-25 = Run**

Use this as a conversation starter, not a definitive assessment. The qualitative evidence from
the stage descriptions above matters more than the number. An organization scoring 14 might be
solidly in Walk — or might be a Crawl organization that overrates itself. Validate scores against
the stage-exit criteria.

Most organizations are in Crawl whether they realize it or not. Only a small percentage have
genuinely reached Walk. Run organizations are exceptional.

## Communication Guidelines

**For organizations in Crawl:**
- Validate their starting point — Crawl is where everyone begins
- Emphasize patience — rushing creates gaps that haunt later stages
- Focus on observable, quick-win improvements that build confidence
- Don't overwhelm with advanced concepts they're not ready for

**For organizations in Walk:**
- Challenge their assumptions — are they truly in Walk or Crawl with different teachers?
- Encourage experimentation and adaptation over copying
- Push for judgment over rules
- Surface where capabilities are still in Crawl despite overall Walk positioning

**For organizations approaching Run:**
- Stop benchmarking against frameworks
- Focus on what's unique about their approach
- Explore where depth remains even in "mastered" areas
- Celebrate what they've built while identifying remaining growth
