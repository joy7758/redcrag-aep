# Platform Embedding Notes

## OpenTelemetry

Use OpenTelemetry-style spans as the lowest-friction source of execution traces. The demo converter maps spans with `tool.name`, `receipt_id`, `risk_level`, `human_review.approved`, and `source_clause_ref` into AEP fields.

## Langfuse

Langfuse can be treated as a trace source. The integration should export selected trace events into AEP, then add RedCrag validation on top. Do not store prompts or sensitive source text in AEP unless the pilot explicitly approves it.

## CozeLoop

CozeLoop can be treated as an LLM engineering trace and evaluation source. The RedCrag layer should map key agent actions, review decisions, and receipts into AEP rather than duplicating the whole platform.

## MCP Tool Plugins

MCP tools can emit tool-call metadata directly: purpose, risk level, receipt ID, output reference, and human-review state. This keeps the AEP package close to the actual agent action boundary.

## Why Not Start With a Large SaaS

The first proof should show that evidence can be generated, signed, validated, and failed in a controlled way. A large SaaS surface would add account, billing, hosting, tenant, and compliance claims before the core evidence model is proven.
