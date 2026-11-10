# LLM Workflow Architecture

Principles for any workflow where an LLM makes subjective or strategic decisions (QA evaluation, creative judgment, report generation, campaign actions). Adapted from a colleague's operating contract, 2026-08-26.

**Inspect the exact model input and output before changing code.** When a workflow regresses, trace from first source of truth forward: stored prompt/context → exact LLM input → exact LLM output → parser/schema → renderer → published output.

**If the output is bad but structurally valid, fix the prompt side, not the code side:** improve the prompt, context, canonical primitives, taste principles, examples, or output contract. Do not add code-based judgment. One strong prompt beats an overengineered pipeline.

**Identify reusable decision primitives** — components, image styles, ad formats, hooks, scenes, proof types, audience segments, editing operations, campaign actions, publishing targets. **Keep ONE canonical runtime source of truth per primitive** (name, purpose, examples of when useful). Do not duplicate domain judgment across code, prompts, schemas, validators, and UI labels.

**Code checks are for objective facts only:** required fields, source preservation, schema shape, auth, runtime errors, broken assets, invalid URLs, publishing/deployment state, platform constraints. **Never build deterministic validators for taste** — persuasion, beauty, creativity, rhythm, narrative quality, visual judgment. Improve prompts, examples, context, and review instructions instead.

**Don't leak process language into creative prompts.** Model-facing prompts describe desired output, decision criteria, taste, constraints, and available primitives — not your internal pipeline vocabulary.

**Prefer simple contracts:** raw input + canonical primitives + taste/quality principles + required output schema. Avoid multi-pass pipelines unless a specific observed failure proves the split necessary (and the change is approved).

**Source content is a hard contract.** Models may structure, emphasize, split, and arrange exact content; they must not silently rewrite, invent, remove, or duplicate source meaning unless explicitly asked.

**A conversational prompt (an interview, an intake chat) needs an explicit reply budget.** Without one, a strong model recaps everything agreed so far before each question. In the first real brand interview (2026-10-19) that meant about 25,000 words of recaps across 62 turns, which the person mostly rubber-stamped, and a 4 h 13 min session against a 25–35 min promise. State the budget ("one sentence of acknowledgement, then the next question, under 80 words, no recaps or tables") and name where checking happens instead, such as a later review step. Prove a prompt change by replaying a real transcript's user turns through the new prompt and comparing reply lengths with the original, before any real user meets it.

**A model does not agree with itself, so measure a change against its self-agreement, never against 100%.** Run the unchanged system twice over the same inputs first and record how often the two runs reach the same outcome. One video QA worker agreed with itself on 88.6% of task outcomes (70 of 79; 97.2% per gate), so any comparison between two versions of it reads inside that noise, and a new version that matches the old on 89% of tasks has not changed anything measurable. When comparing outputs, match the schema and the critical values (the verdict, the status) exactly, and free-form model text by intent only ("did substantive reasoning land in the field?"): a string diff of model prose is all false alarms.

**Push back when a proposed fix adds control before understanding.** First ask: is this a prompt/source-of-truth problem, a model-output problem, or an objective code/runtime problem?
