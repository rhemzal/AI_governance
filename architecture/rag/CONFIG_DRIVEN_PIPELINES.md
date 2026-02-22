# Configuration-Driven / Pipeline-Declarative Architecture — Advisory Note

_Provenance: This document originates from the AI_governance kit (https://github.com/rhemzal/AI_governance). If you copied it into another repository, keep this line to preserve traceability._

## Core Idea
Systems where architecture decisions — components, connections, behavior parameters — are expressed **declaratively in configuration files** (YAML/JSON/TOML), and code serves as a **generic, thin runtime** that interprets and executes the configuration.

The configuration IS the architectural contract; the runtime merely enforces it.

## Why It Helps
- **Separation of concerns**: "what" (config) is decoupled from "how" (runtime code).
- **Easier onboarding**: a new developer reads config to understand the topology, not code.
- **Config-level swapability**: swap components, parameters, or connections by editing config, not code.
- **Predictability**: the system's behavior is inspectable without running it (if config is well-structured).
- **Reuse**: the same runtime can serve many different pipeline configurations.

## When to Choose It
- AI/ML pipelines where topology and component selection are the primary design axes.
- Data processing systems where the "domain" is pipeline connectivity, not business rules.
- Template-based systems where each configuration produces an independent deployable unit.
- Systems operated by domain experts who should not need to touch code.
- Environments where the set of components is stable but their wiring changes frequently.

## When NOT to Choose It
- When domain logic is complex and cannot be expressed declaratively (conditionals, loops → use code).
- When configuration grows until it IS code (Turing-complete YAML anti-pattern).
- When you need fine-grained, code-level boundary enforcement across many business rules.
- When the pipeline topology is fixed and never changes (no benefit over direct code).

## Common Failure Modes
- **Schema drift**: config structure changes without versioning or validation; old configs silently break.
- **Magic constructors/tags in YAML**: e.g., `!pw.xpacks.llm.llms.OpenAIChat` — creates tight coupling hidden inside configuration files, which is invisible to static analysis.
- **Config-as-code anti-pattern**: configuration grows until it contains conditionals and loops, losing all declarative benefits.
- **No config validation at load time**: invalid configs fail at runtime or silently produce wrong results instead of failing fast at startup.
- **Testing gap**: config is never tested independently from code; broken wiring is only discovered during execution.
- **Undocumented defaults**: behavior depends on implicit defaults that are not visible in config, creating invisible coupling.

## Heuristics
- **Validate strictly at load time (fail-fast)**: reject any config that does not match the schema before execution begins. Use `additionalProperties: false` (JSON Schema) or `extra="forbid"` (Pydantic) — see Concrete Example below.
- **Version config schemas at boundaries**: apply the same discipline as API schemas; treat a config schema change as a contract change (see `SCHEMA_EVOLUTION_AND_VERSIONING.md`).
- **Test config independently**: "does this YAML parse correctly?", "are all referenced components valid and available?", "does this config produce the expected pipeline topology?".
- **Keep config declarative**: if you need conditionals or loops in config, that logic belongs in code or in a dedicated orchestration layer.
- **Audit magic constructors**: any YAML tag or constructor that invokes code is an implicit coupling; document it explicitly and test it.

## Concrete Example: Fail-Fast Config Boundary

Using Pydantic's `ConfigDict(extra="forbid")` as a load-time boundary contract (aligns with `constitution/AI_RULES.md` §2.3 — fail-fast validation):

```python
from pydantic import BaseModel, ConfigDict
from enum import Enum

class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

class PipelineConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")  # reject unknown keys immediately

    llm_provider: LLMProvider
    embedding_model: str
    chunk_size: int = 512
    top_k: int = 5
```

Any config key not in the schema raises a `ValidationError` at load time — not at inference time. This is the boundary contract.

## Related Documents
- `architecture/ARCHITECTURE_DECISION_FRAMEWORK.md`
- `architecture/ARCHITECTURE_STYLE_MATRIX.md`
- `architecture/rag/SCHEMA_EVOLUTION_AND_VERSIONING.md`
- `architecture/rag/INFORMATION_HIDING.md`
