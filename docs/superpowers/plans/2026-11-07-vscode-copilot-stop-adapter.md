# VS Code Copilot Stop Adapter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Tier C Stop integration for VS Code with the GitHub Copilot harness, including safe installation, verification, and operator instructions.

**Architecture:** Keep the existing Cursor adapter and add an independent VS Code Copilot `agentStop` adapter using the documented repository hook format. A Python standard-library script will consume the Copilot event, run the existing agent-boundary verifier, and emit the Copilot decision shape; the opt-in installer will install it and idempotently add the VS Code skill/instruction route without replacing host files.

**Tech Stack:** Bash, Python 3 standard library, JSON, `unittest`, Markdown.

**Spec:** `governance/experimental/spec_gates/OPT_IN_STACK.md` and `usage/ADOPTION_SCOPE_AND_HOSTS.md`; host contract: https://code.visualstudio.com/docs/agent-customization/hooks and https://docs.github.com/en/copilot/reference/hooks-reference

## Global Constraints

- Keep all Tier C material experimental and excluded from import bundles.
- Preserve existing host instructions and hook configuration; only add a uniquely named route/config when absent.
- VS Code support targets the VS Code Copilot harness and its preview hook experience; do not claim support for Local, Claude, Codex, or cloud sessions.
- The verifier is a Bash script; Windows hook configuration may launch the Python adapter through PowerShell, but Bash must also be available on `PATH`.
- The hook runs `.specify/gates/verify.sh --boundary agent`; its output must be exactly one JSON decision object on stdout, with diagnostics on stderr.
- A passing verifier allows stop; a verifier failure blocks once with bounded evidence; `stop_hook_active` prevents an unbounded continuation loop.
- Native host dispatch must be verified in a real VS Code Copilot session; unit tests and file presence are not dispatch evidence.
- Do not commit, push, merge, or deploy as part of this task.

## Review Focus

- Verifier exit 0 must allow stop; a fake passing verifier pins the expected `{}` result.
- Verifier exit 2 must block with the last 6000 characters of output; a long fake failure pins the output bound and tail.
- Missing verifier, other verifier exit codes, and timeout must request an UNVERIFIED report; follow-up input with `stop_hook_active: true` must allow stop.
- Invalid or non-object hook input must produce an explicit diagnostic and must not emit malformed JSON.
- Hook execution must use the configured repository root and must not pass VS Code/Cursor project-root environment variables into the verifier.
- Invalid verifier output bytes must not prevent the adapter from emitting a valid JSON decision.
- Checker fixtures must reject inert launch commands, and an installed hook must remain executable.
- The checker must reject a Copilot hook timeout that does not exceed the adapter's verifier timeout.

---

```aep
{
  "schema_version": 1,
  "status": "READY",
  "objective": "Add an opt-in VS Code Copilot agentStop adapter to the Tier C stack without changing the existing Cursor contract.",
  "discovery": [
    "Baseline: existing Cursor Stop contract tests pass (6 tests); Tier C installer tests pass (5 tests).",
    "Gap: Tier C installer/checker and adoption docs only describe Cursor Stop; VS Code CLI is unavailable here, so native dispatch cannot be tested in this environment.",
    "Compatibility: current Cursor adapter uses loop_count/followup_message; VS Code Copilot uses repository .github/hooks/*.json, agentStop, stop_hook_active, and decision/reason output. VS Code hooks are Preview and session-target-specific.",
    "Method: add a host-specific contract adapter and targeted unit/installer tests; retain existing shell verifier and do not extract or alter the Cursor implementation."
  ],
  "risk": "HIGH",
  "scope": {
    "paths": [
      ".github/hooks/ai-governance.json",
      ".github/hooks/kit-verify-stop.py",
      ".github/skills/governed-work/SKILL.md",
      ".gitignore",
      "governance/experimental/spec_gates/install-opt-in-stack.sh",
      "governance/experimental/spec_gates/check-opt-in-stack.sh",
      "governance/experimental/spec_gates/install-vscode-adapter.py",
      "governance/experimental/spec_gates/templates/copilot-instructions-opt-in.md.template",
      "governance/experimental/spec_gates/README.md",
      "governance/experimental/spec_gates/OPT_IN_STACK.md",
      "ci/gate_tests/test_vscode_stop_hook_contract.py",
      "ci/gate_tests/test_install_opt_in_stack.py",
      "ci/gate_tests/test_claim_cards.py",
      "ci/claim_cards.json",
      "usage/ADOPTION_SCOPE_AND_HOSTS.md",
      "usage/FULL_OPT_IN_ADOPTION_PLAYBOOK.md",
      "usage/HOW_TO_IMPORT.md",
      "adr/ADR_0019_VS_Code_Copilot_Stop_Adapter.md"
    ],
    "allowed_effects": [
      "Edit the AI_governance working tree",
      "Run bounded repository-local tests and disposable installer fixtures",
      "Create and remove an isolated Docker smoke image and fixture with no repository mount or runtime network",
      "Inspect pinned Harbor applicability without running paid agent trials or using credentials"
    ],
    "approval_required": ["Commit", "Push", "Merge", "Deploy"]
  },
  "steps": [
    {
      "paths": [".github/hooks/kit-verify-stop.py", "ci/gate_tests/test_vscode_stop_hook_contract.py"],
      "action": "Add tests first for allow, block, bounded failure output, unavailable verifier, active-loop guard, invalid input, invalid verifier bytes, and environment isolation; implement the Copilot agentStop adapter only after the tests fail.",
      "reason": "The host output contract differs from Cursor, and continuation behavior must remain bounded."
    },
    {
      "paths": [".github/hooks/ai-governance.json", "governance/experimental/spec_gates/templates/copilot-instructions-opt-in.md.template", ".github/skills/governed-work/SKILL.md", ".gitignore", "governance/experimental/spec_gates/install-opt-in-stack.sh", "governance/experimental/spec_gates/check-opt-in-stack.sh", "ci/gate_tests/test_install_opt_in_stack.py", "ci/gate_tests/test_claim_cards.py"],
      "action": "Install the executable hook, preserve pre-existing VS Code instructions/configuration and adapter mode, add the skill route idempotently, and extend stack checks to reject inert commands or a host timeout no longer than the verifier timeout.",
      "reason": "A runtime script without an installed hook or active Copilot route does not deliver Tier C behavior."
    },
    {
      "paths": ["governance/experimental/spec_gates/README.md", "governance/experimental/spec_gates/OPT_IN_STACK.md", "usage/ADOPTION_SCOPE_AND_HOSTS.md", "usage/FULL_OPT_IN_ADOPTION_PLAYBOOK.md", "usage/HOW_TO_IMPORT.md", "adr/ADR_0019_VS_Code_Copilot_Stop_Adapter.md", "ci/claim_cards.json", "ci/gate_tests/test_claim_cards.py"],
      "action": "Document the preview/session-target limits, manual native-dispatch verification and evidence, update Tier C host claims, and record the architecture decision and contract claim.",
      "reason": "Operators must not infer native hook execution from static checks or tests."
    }
  ],
  "verification": [
    {
      "command": "timeout 60s python3 -m unittest discover -s ci/gate_tests -p 'test_vscode_stop_hook_contract.py' -q",
      "expected": "All VS Code adapter contract tests pass."
    },
    {
      "command": "timeout 120s python3 -m unittest discover -s ci/gate_tests -p 'test_install_opt_in_stack.py' -q",
      "expected": "Installer regression tests pass, including preservation and idempotency."
    },
    {
      "command": "timeout 120s python3 -m unittest discover -s ci/gate_tests -q",
      "expected": "The complete repository-local gate suite passes."
    },
    {
      "command": "git diff --check",
      "expected": "No whitespace errors."
    }
  ],
  "acceptance": [
    "A disposable Tier C install contains a valid VS Code Copilot agentStop hook, executable adapter, and governed-work route without replacing existing host files.",
    "The hook follows the Copilot agentStop contract, invokes the existing verifier, bounds follow-up output, and does not continue indefinitely.",
    "The stack checker distinguishes configured files from verified native VS Code dispatch.",
    "Tier C docs identify VS Code Copilot hooks as Preview and provide a fresh-session dispatch check; no native-dispatch claim is made without a VS Code session."
  ],
  "blocking_questions": [],
  "budget": {
    "max_repair_attempts": 2,
    "on_exhaustion": "Stop the affected action and report the failing command, evidence, and smallest next decision."
  },
  "doc_delta": "Update Tier C installation, host eligibility, verification, and limitations to describe the VS Code Copilot Stop adapter alongside Cursor."
}
```

### Task 1: Copilot agentStop contract

**Files:**
- Create: `.github/hooks/kit-verify-stop.py`
- Create: `ci/gate_tests/test_vscode_stop_hook_contract.py`
- Create: `.github/hooks/ai-governance.json`

**Interfaces:**
- Consumes: Copilot `agentStop` JSON on stdin; `.specify/gates/verify.sh --boundary agent`.
- Produces: `{}` to allow stop or `{"decision":"block","reason":"..."}` to require one bounded follow-up.

- [ ] **Step 1: Write the failing contract tests** for the five Review Focus cases, including exact JSON output shapes and stderr diagnostics.
- [ ] **Step 2: Run the targeted test** with `timeout 60s python3 -m unittest discover -s ci/gate_tests -p 'test_vscode_stop_hook_contract.py' -q`; it must fail because the adapter is absent.
- [ ] **Step 3: Implement the standard-library Python adapter**. Read stdin once, use the configured repository root (`cwd` is `"."`), run the verifier as an argument list with a bounded timeout, sanitize inherited project-root variables, and emit exactly one JSON object. Use the `stop_hook_active` input as the loop guard.
- [ ] **Step 4: Add the hook configuration** with version 1, `agentStop`, `type: command`, Bash/Python and PowerShell/Python launch commands, repository-root `cwd`, and a timeout longer than the verifier's own timeout.
- [ ] **Step 5: Rerun the targeted contract test** and require all cases to pass.

### Task 2: Tier C installer and completeness checks

**Files:**
- Modify: `governance/experimental/spec_gates/install-opt-in-stack.sh`
- Modify: `governance/experimental/spec_gates/check-opt-in-stack.sh`
- Modify: `ci/gate_tests/test_install_opt_in_stack.py`
- Modify: `.gitignore`
- Create: `governance/experimental/spec_gates/install-vscode-adapter.py`
- Create: `governance/experimental/spec_gates/templates/copilot-instructions-opt-in.md.template`
- Copy: existing `.github/skills/governed-work/SKILL.md` into the adopter through the installer.

**Interfaces:**
- Consumes: Task 1 hook config and script; existing Tier C `KIT_SOURCE` and installer conventions.
- Produces: Repeatable VS Code/Copilot Tier C installation that preserves host files and reports configured status without claiming native dispatch.

- [ ] **Step 1: Add failing installer fixture assertions** for hook/script installation, preservation of existing `.github/copilot-instructions.md` and hook files, and idempotent route insertion.
- [ ] **Step 2: Run the targeted installer test** with `timeout 120s python3 -m unittest discover -s ci/gate_tests -p 'test_install_opt_in_stack.py' -q`; it must fail on the missing VS Code integration.
- [ ] **Step 3: Extend stack installation** to invoke the tested adapter installer, copy only missing VS Code files, append the route block only once, preserve existing host config, and add recorder files to `.gitignore`.
- [ ] **Step 4: Extend the checker** to report the VS Code Copilot route and hook configuration separately from real native dispatch evidence.
- [ ] **Step 5: Rerun installer tests** and require preservation/idempotency checks to pass.

### Task 3: Adoption contract and documentation

**Files:**
- Modify: `usage/ADOPTION_SCOPE_AND_HOSTS.md`
- Modify: `usage/FULL_OPT_IN_ADOPTION_PLAYBOOK.md`
- Modify: `usage/HOW_TO_IMPORT.md`
- Modify: `governance/experimental/spec_gates/README.md`
- Modify: `governance/experimental/spec_gates/OPT_IN_STACK.md`
- Modify: `ci/claim_cards.json`
- Create: `adr/ADR_0019_VS_Code_Copilot_Stop_Adapter.md`

**Interfaces:**
- Consumes: Tested hook and installer behavior from Tasks 1–2.
- Produces: One consistent Tier C definition for Cursor and VS Code Copilot, with preview/runtime limits and native-dispatch evidence requirements.

- [ ] **Step 1: Update host/tier tables and installation instructions** to require the Copilot session target for VS Code and state that VS Code hooks are Preview.
- [ ] **Step 2: Document native dispatch proof** using a fresh VS Code session, the Copilot Hooks output channel or ignored recorder marker/log, and clearly distinguish this from contract tests and file checks.
- [ ] **Step 3: Add ADR-0019 and a claim card** tied to the contract test; state that host-specific native dispatch remains a manual adoption check.
- [ ] **Step 4: Run `timeout 120s python3 -m unittest discover -s ci/gate_tests -q` and `git diff --check`;** require all tests to pass and no whitespace errors.

### Task 4: Container verification and Harbor boundary

**Files:**
- Modify: `governance/experimental/spec_gates/OPT_IN_STACK.md`

**Interfaces:**
- Consumes: Task 1 adapter contract, Docker daemon, pinned Harbor 0.25.0 CLI, existing Harbor job definitions.
- Produces: An isolated Docker process smoke result and explicit guidance distinguishing container/Harbor evidence from native VS Code dispatch.

- [ ] **Step 1: Run a temporary Docker smoke** with only the adapter and a controlled fake verifier in the image; exercise verifier allow and block, with the test container on `--network none` and no repository mount.
- [ ] **Step 2: Inspect Harbor's existing agent/job types** and do not treat oracle/nop or Cursor CLI trials as VS Code Copilot hook evidence.
- [ ] **Step 3: Document the verification layers** and retain a fresh VS Code Copilot session as the only native dispatch proof.
- [ ] **Step 4: Rerun the full gate suite and `git diff --check`.**

## Execution handoff

Plan status: **READY**. Native VS Code dispatch cannot be exercised in this environment because the VS Code CLI is unavailable. Docker can verify process behavior only; the existing Harbor tasks do not dispatch VS Code Copilot hooks. Keep host-level dispatch unverified until a fresh native session produces corroborating evidence.

Verification addendum status: **PARTIAL**. Docker daemon is available and Harbor 0.25.0 resolves through `uvx`, but the isolated Docker smoke command was denied by the pre-tool hook (exit code 2) before execution. Do not infer a Docker result; the native VS Code check remains a manual adoption step.
