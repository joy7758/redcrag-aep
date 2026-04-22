# Contribution Statement

## One-sentence Contribution

This prototype introduces a minimal Risk-linked Agent Evidence Profile (AEP) that connects pre-execution security findings with runtime execution evidence to support verifiable accountability in FDO and data-space environments.

## Problem Gap

Security scanners can identify potential risks in agent configurations, tools, or runtime settings. These findings are useful before execution because they describe what may go wrong, such as an over-permissioned tool or a risky runtime capability.

However, scanner findings alone do not prove what happened during a concrete execution. A scanner can report that `write_file` is risky, but it cannot by itself show whether a specific agent run attempted that tool, whether policy blocked it, or whether the run remained within acceptable bounds.

Runtime logs alone often lack integrity structure, policy linkage, and risk linkage. They may show that actions occurred, but without a stable evidence profile they are harder to validate, preserve, or reference as accountable execution evidence.

The gap is the missing bridge between potential risk and actual execution evidence.

## Proposed Contribution

The AEP bundle acts as a manifest-level evidence object. It identifies the agent, execution, policy, scanner findings, event log, and integrity metadata for one run.

The AEP event log acts as an execution-level trace. Each event records a tool-call attempt, policy decision, execution status, input and output hashes, risk references, and hash-chain metadata.

`risk_links` bridge scanner findings to execution evidence at the bundle level, while `risk_refs` identify which findings were touched by specific events. The validator turns this evidence into `PASS`, `WARN`, or `FAIL` conclusions.

## Research Claim

The prototype demonstrates that a small evidence profile can distinguish between potential risk, non-triggered risk, and triggered policy violation in a deterministic agent execution setting.

## What This Is Not

- not a scanner replacement
- not an agent security platform
- not a production compliance system
- not a full FDO implementation
- not a real-world benchmark
