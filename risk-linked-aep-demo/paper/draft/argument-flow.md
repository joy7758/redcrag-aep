# Argument Flow

## Core Claim

A small evidence profile can connect scanner findings with runtime execution evidence and support reviewable accountability decisions.

## Argument Chain

1. Agent scanners identify possible risks.
2. Possible risks alone do not prove what happened.
3. Agent runtime evidence records concrete behavior.
4. Runtime evidence needs integrity and policy context to be reviewable.
5. Risk linkage connects possible risk to actual tool attempts.
6. Validator rules convert evidence into PASS/WARN/FAIL.
7. FDO/data-space object shaping supports future preservation and reference.

## Key Distinction

Potential risk is not the same as triggered violation.

Examples:
- WARN: high-risk `write_file` finding exists, but `write_file` is not attempted.
- FAIL: high-risk `write_file` finding exists, and `write_file` is attempted.

## Boundary Statement

The work is not a scanner replacement, not a security platform, and not a production compliance system.

## Reviewer Risk

- Is this only logging? It is more than raw logging because the event trace is hash-chained, bound to a bundle, linked to policy, and linked to risk findings.
- Why is hash chaining needed? Hash chaining makes event order and event content reviewable for consistency.
- Why not just use scanner output? Scanner output describes potential risk but does not prove what happened in a concrete execution.
- Why does a blocked denied action count as FAIL? The attempted denied action is itself policy-violation evidence even if enforcement prevents actual execution.
- How does this relate to FDO/data spaces? The bundle is shaped as an evidence object with identifiers, profile metadata, integrity references, policy references, and risk links.
- What is new beyond provenance? The contribution is the explicit linkage between pre-execution risk findings, policy decisions, runtime tool attempts, and PASS/WARN/FAIL validation.
