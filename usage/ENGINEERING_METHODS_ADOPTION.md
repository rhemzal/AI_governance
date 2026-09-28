# Engineering Methods in Existing Projects

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If copied, preserve this line._

## Scope and authority

This guide turns the [method selector](AI_ENGINEERING_METHODS.md) into a small, reviewable
change in an existing project. It is advisory implementation guidance. The behavioral
minimum is in `constitution/AI_RULES.md` §6.5; local policy promotes specific controls.
Importing files does not activate checks, grant tool access, or establish effectiveness.

Both this guide and the selector are in **minimal**. Focused method guides and CI tools
are **standard** or optional upstream material from the same pinned revision. The research
ledger is optional `research/AI_ENGINEERING_METHODS_EVIDENCE.md` (`research` bundle).

## 1. Locate the actual adoption boundary

Inspect the project's active instruction entry points, kit revision/selection, local
overlay, test commands and workflows. Identify which instructions each enabled agent
actually loads; a nested imported AGENTS file is not automatically an active entry point.
An agent with no working instruction route needs host integration, not more kit files.

| Existing setup | Smallest safe update |
| --- | --- |
| Copy pinned under a kit directory | Prepare and verify a fresh candidate snapshot; compare old/new/local changes; preserve host files and merge the entry-point delta |
| Git submodule | Review the pin change and host instruction/overlay delta together; preserve declared adoption scope |
| Fork or modified imported files | Reconcile changes against the recorded upstream ancestor; retain explicit local decisions; do not overwrite them to make a comparison pass |
| Root-layout copy / unknown provenance | Inventory ownership first; identify conflicting local rules; migrate one reviewed snapshot without deleting unclassified files |
| Reference URL only | Assess applicability; obtain authorization for a baseline import before presenting it as adopted |

For copy mechanics use `usage/HOW_TO_IMPORT.md` in standard or the pinned upstream checkout.
Neither an old version nor a lower CM justifies a whole-project rewrite. An upstream PR
cannot compel repositories that have not adopted its revision. A dependency bot may propose
pin updates if already available; automatic policy activation is not the default.

## 2. Establish a baseline on one real slice

Pick a recurring task or material risk: one adapter contract, one GUI journey, one field
failure, or one flaky test boundary. Inspect the existing code and command before adding
a wrapper, tool or test framework.

Record in the existing task record/overlay:
- observed failure or friction, starting revision, environment and current verification;
- one outcome to improve and behavior/contracts that must remain compatible;
- chosen smallest method, why the existing approach is insufficient, and what is deferred;
- a representative task, expected observation, owner, effort/repair budget and review trigger.

For a small task, a few lines suffice. When the existing approach works, **keep it**.
No persistent method inventory is needed unless the project is coordinating a rollout.

If the baseline cannot run, record why. Repair the environment or use a bounded, explicitly
partial observation. Do not label a missing/failed/skipped check as a passing baseline.
Characterization tests describe current behavior; they do not legitimize a known defect.

## 3. Pilot, then decide

| State of one selected practice | Evidence / action | Enforcement |
| --- | --- | --- |
| Deferred | No current need, or unmet prerequisite; name a revisit trigger | No new obligation; existing rules still apply |
| Pilot | Use on a real scoped task; preserve before/after evidence and a known-bad control where practical | Existing local checks/review; no new mandatory job |
| Adopted | Outcome improved or a concrete risk is now detectable; owner accepts maintenance cost | Stable host command and discoverable instructions |
| Required in a declared scope | Check detects the intended bad case, passes good cases, and has tolerable runtime/noise | Existing verifier/CI invokes it for that scope; missing execution is not success |
| Retired | Removal trial preserves required outcomes; update references and policy deliberately | Remove redundant scaffolding; retain underlying invariant/control |

These are practice states, **not a third maturity scale** alongside G and CM. Promotion
does not require advancing an entire repository's CM. Existing normative timing still
applies; use an approved local override/waiver if an already-required rule cannot be met.
Start with one practice; follow the adaptive limit of at most two new process requirements
per change. A successful pilot is evidence for that task class, not universal reliability.

Use an optional small table in the **existing** project overlay, not another policy file:

| Outcome / scope | State | Host verification / invocation | Evidence | Owner / review trigger |
| --- | --- | --- | --- | --- |
| Example: preserve stream-reset contract in playback adapter | Pilot | Existing adapter test target; run for changes to implementation **or its callers/config** | Base/head results and fixture revision | Component owner; review after representative reset fixes |

Replace examples with actual paths/commands before activating a requirement. Put persistent
exceptions in the existing waiver mechanism; a task-local explanation cannot waive a
mandatory invariant. Use the project’s existing decision process, not an extra approval round.

## 4. What actually enforces adoption

| Mechanism | Enforces | Does not prove |
| --- | --- | --- |
| Agent instructions + task evidence | Declared method, scope, acceptance and deviations, subject to review | That an agent followed every instruction |
| Existing local verifier | The properties its executed checks cover | That every contributor ran it |
| Existing CI / required status when locally authorized | Check execution and selected outcomes on a revision | Correct intent, completeness, or production behavior outside coverage |
| Tool permissions / isolated environment | Actual access and effect boundaries | Business correctness |
| Review of artifacts and pilot outcomes | Whether the selected method helps this task class | A universal productivity increase |

Use the lightest sufficient combination. For repeatable mandatory invariants, integrate
with the actual merge/release path only under the project's authority. A local hook is
bypassable; a workflow file alone is not branch protection. Do not require a new reviewer,
cloud service, dashboard, MCP server, or agent just to declare adoption.

## 5. Legacy debt: prevent new violations without freezing development

Use existing scanner baseline support when it has the required semantics. Otherwise the
optional standard-library `ci/ratchet_findings.py` compares **sets of stable finding IDs**.
It permits inherited findings in the agreed scope while rejecting newly introduced ones.
It never runs project commands, writes reports, updates a baseline, or installs a gate.

This is a migration aid, not a waiver of mandatory rules or a mechanism for grandfathering
critical security defects. Treat such defects through existing risk/waiver/incident policy.

### Scanner report contract (schema 1)

Both JSON inputs contain exactly these fields (illustrative values):

```json
{
  "schema_version": 1,
  "revision": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "check": "python-boundaries@1+rules-sha256:example",
  "scope": ["src/core"],
  "status": "ok",
  "findings": ["no-adapter-import:src/core/orders.py:load:adapters.db"]
}
```

- `revision`: full lowercase Git commit ID for the clean tree actually scanned; an
  uncommitted tree is not eligible for this commit-bound comparison.
- `check`: stable identity including scanner **version, rules, configuration and ID
  normalization**. Both reports use the same trusted scanner contract.
- `scope`: nonempty set of explicit repository-relative roots (or `.` for the whole tree).
  Scope is identical on both sides; broad dependency effects need a broad enough scope.
- `status`: `ok` means the scanner completed for the entire declared scope. Findings may
  exist. Do not confuse a scanner's documented “findings detected” exit with execution
  failure; do not convert timeout, unavailable tools, parse errors or skipped files into `ok`.
- `findings`: possibly empty list of unique IDs. Include rule/path/symbol/target or equivalent
  discriminators; counts or rule names alone hide replacement violations. Prefer stable
  semantic locations to line numbers. Renames/normalization changes need explicit review.

### Wiring into an existing verifier

1. Resolve a trusted comparison base (usually the target branch or reviewed baseline)
   and tested head independently of the reports. Use clean isolated checkouts.
2. Run the same approved host scanner/normalizer over the same scope at both revisions.
   Obtain the base report from the trusted base run, not a candidate-edited baseline file.
3. Propagate scanner failures. Only emit `status: ok` after successful complete scanning.
4. Run the comparator, using independently resolved full commit IDs:

```bash
python3 "$KIT_SOURCE/ci/ratchet_findings.py" \
  --baseline "$BASE_REPORT" --current "$HEAD_REPORT" \
  --baseline-revision "$BASE_SHA" --current-revision "$HEAD_SHA"
```

Set these variables to reviewed paths/revisions; the command is a wiring example, not an
installed host scanner. Exit **0** = no new findings (possibly remaining debt), **1** =
new findings, **2** = invalid/incomparable input. Both nonzero exits fail an activated check.
The output lists introduced, resolved and remaining IDs; it never says the project is clean.

5. Demonstrate one existing-debt pass, one true improvement, and one injected new violation
   in disposable fixtures. Include equal-count replacement and scanner-error controls.
6. Protect the comparator, scanner/configuration, scope and baseline provenance through the existing
   review/CI trust boundary. The comparator validates declarations; it cannot authenticate
   a claimed revision, prove scan completeness, or detect a dishonest empty report.
7. Recompute from the trusted current base on later PRs, or deliberately advance a reviewed
   stored baseline after merge. Otherwise a fixed old baseline can allow resolved debt to
   reappear. Scope/rule/normalizer migrations require reviewed rebaselining, not auto-accept.

Test only changed lines when the invariant is truly local. Caller changes, shared schemas,
renames and configuration can violate a contract without editing the old finding's line.
A security-critical regression never becomes acceptable just because the total count fell.

## 6. Worked adoption choices

| Situation | First useful change | Proof / what stays deferred |
| --- | --- | --- |
| Legacy backend without reliable unit isolation | Characterize one public boundary using existing fixtures; introduce only the seam needed for the change | Intended change and compatibility controls; whole-core refactor deferred |
| GUI + backend state disagreement | Correlate one action with backend/session state using existing CLI/socket/log interfaces | Repeat the action and observe both ends; MCP only if it improves access materially |
| Intermittent device failure | Redacted state capture and one repeatable diagnostic with explicit device ownership | Known-good/bad comparison on representative hardware when needed; fleet platform deferred |
| Agent repeatedly uses the wrong build command | Fix the active host instruction pointer and verify the command | Fresh task finds and uses it; another wrapper or repository encyclopedia deferred |
| Boundary violations already exist | Pilot a scoped no-new-findings check with the trusted base protocol above | Replacement violations and scanner failures fail; bulk cleanup separate |

These are illustrative choices, not assessments of any named downstream repository.

## 7. Close the loop

At pilot review, keep, adjust, defer or remove the method. Compare accepted behavior, missed
regressions, repair/review burden, unnecessary changes, and cost when observable. Reuse
existing PR/run evidence; do not claim productivity gains from a green comparator or one task.
An ineffective required check is changed by an authorized policy change or waiver, never
silently bypassed by the agent it constrains.

For a governance update, record old SHA → new SHA, adopted scope, host instruction changes,
activated checks, deliberate deferrals, pilot evidence and rollback. Completion means a
fresh task can discover and use the selected path; merely copying the newest kit is partial.

## Related Documents

- [Method selection](AI_ENGINEERING_METHODS.md)
- `constitution/AI_RULES.md` §6.5
- `constitution/ADAPTIVE_GOVERNANCE.md`
- Standard / optional upstream: `usage/HOW_TO_IMPORT.md`, `usage/AGENT_EVALUATION.md`,
  `usage/ADOPTION_ENFORCEMENT_CONTRACT.md`, `usage/GOVERNANCE_WAIVERS.md`,
  `governance/LOCAL_OVERLAY_TEMPLATE.md`, `ci/ratchet_findings.py`
