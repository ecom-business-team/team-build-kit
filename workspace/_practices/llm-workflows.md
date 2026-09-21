# LLM Workflow Architecture

Principles for any workflow where an LLM makes subjective or strategic decisions (QA evaluation, creative judgment, report generation, campaign actions). Adapted from a colleague's operating contract, 2026-08-26.

**Inspect the exact model input and output before changing code.** When a workflow regresses, trace from first source of truth forward: stored prompt/context → exact LLM input → exact LLM output → parser/schema → renderer → published output.

**If the output is bad but structurally valid, fix the prompt side, not the code side:** improve the prompt, context, canonical primitives, taste principles, examples, or output contract. Do not add code-based judgment. One strong prompt beats an overengineered pipeline.

**Identify reusable decision primitives** — components, image styles, ad formats, hooks, scenes, proof types, audience segments, editing operations, campaign actions, publishing targets. **Keep ONE canonical runtime source of truth per primitive** (name, purpose, examples of when useful). Do not duplicate domain judgment across code, prompts, schemas, validators, and UI labels.

**Code checks are for objective facts only:** required fields, source preservation, schema shape, auth, runtime errors, broken assets, invalid URLs, publishing/deployment state, platform constraints. **Never build deterministic validators for taste** — persuasion, beauty, creativity, rhythm, narrative quality, visual judgment. Improve prompts, examples, context, and review instructions instead.

**Don't leak process language into creative prompts.** Model-facing prompts describe desired output, decision criteria, taste, constraints, and available primitives — not your internal pipeline vocabulary.

**Prefer simple contracts:** raw input + canonical primitives + taste/quality principles + required output schema. Avoid multi-pass pipelines unless a specific observed failure proves the split necessary (and the change is approved).

**Source content is a hard contract.** Models may structure, emphasize, split, and arrange exact content; they must not silently rewrite, invent, remove, or duplicate source meaning unless explicitly asked.

**Push back when a proposed fix adds control before understanding.** First ask: is this a prompt/source-of-truth problem, a model-output problem, or an objective code/runtime problem?
