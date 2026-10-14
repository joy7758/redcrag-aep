# Clarification Snippets

Purpose:
This file provides candidate wording for later manual polishing. These snippets are not automatically inserted into the paper.

## M1 Mandatory / Optional Field Boundary

- Issue: Mandatory / optional field boundary is not explicit enough.
- Suggested insertion location: Model section, Bundle Model or profile appendix.
- Candidate wording: AEP v0.1 treats the bundle and event fields described in the profile as required for the deterministic validator used in this prototype. Future versions may distinguish required, recommended, and optional fields more formally, but v0.1 uses a minimal required shape to keep validation reviewable.
- Risk if not clarified: Reviewers may ask whether profile fields are normative, illustrative, or validator-specific.
- Freeze-safe? Yes.
- Requires implementation change? No.

## M2 Direct Target-to-Tool Matching

- Issue: risk target -> event.tool matching is intentionally simple but should be explained more clearly.
- Suggested insertion location: Risk Linkage Model or Limitations.
- Candidate wording: The current risk linkage model uses direct matching between a normalized scanner finding target and `event.tool`. This is intentionally simpler than a general capability, permission, endpoint, or SARIF-location mapping. More expressive target namespaces are left to future profile refinement.
- Risk if not clarified: Reviewers may interpret v0.1 as supporting richer target namespaces than it actually supports.
- Freeze-safe? Yes.
- Requires implementation change? No.

## M3 policy_id Trust and Binding Boundary

- Issue: policy_id trust source and external binding are not yet clear.
- Suggested insertion location: Bundle Model, FDO/data-space interpretation, or Limitations.
- Candidate wording: In v0.1, `policy.policy_id` is recorded as review context for validator interpretation. It is not yet bound to an externally registered, signed, or independently resolvable policy object. Future work may bind policy references to governance objects or registry-managed identifiers.
- Risk if not clarified: Reviewers may assume policy objects are externally governed or cryptographically bound.
- Freeze-safe? Yes.
- Requires implementation change? No.

## M4 Collector Trust Assumption

- Issue: Collector trust assumption should be explicit.
- Suggested insertion location: Security and Trust Limits.
- Candidate wording: The prototype assumes that tool calls are mediated by the AEP collector. It does not address bypass resistance, collector compromise, or enforcement outside the instrumented runtime. These assumptions are acceptable for the deterministic prototype but must be revisited before deployment-oriented use.
- Risk if not clarified: Reviewers may read the prototype as providing runtime enforcement against bypass or compromise.
- Freeze-safe? Yes.
- Requires implementation change? No.

## M5 Blocked Action Counts as FAIL

- Issue: Blocked action counts as FAIL needs stronger textual justification.
- Suggested insertion location: Validator-facing semantics or Evaluation interpretation.
- Candidate wording: A denied tool attempt is treated as a policy violation even when the enforcement layer successfully blocks side effects. The reason is that the attempt itself is part of the execution evidence and is relevant to accountability.
- Risk if not clarified: Reviewers may ask why blocked `write_file` is not WARN.
- Freeze-safe? Yes.
- Requires implementation change? No.

## M6 Hashes Are Not Privacy-preserving Disclosure

- Issue: input_hash / output_hash should not be interpreted as privacy-preserving disclosure.
- Suggested insertion location: Security and Trust Limits.
- Candidate wording: Hashing inputs and outputs reduces the amount of raw content stored in the event log, but it is not a privacy-preserving disclosure mechanism. Hashes may still reveal equality, support guessing in small input spaces, or require additional controls such as salting, redaction, or selective disclosure in future versions.
- Risk if not clarified: Reviewers may misread hash storage as a privacy guarantee.
- Freeze-safe? Yes.
- Requires implementation change? No.

## M7 Compress Repeated Caveats

- Issue: Full-paper draft repeats caveats frequently; compress during manual polishing.
- Suggested insertion location: Full paper manual polish.
- Candidate wording: Keep one concise non-claim statement in the introduction, preserve the detailed boundary discussion in the limitations section, and use only a short reminder in the conclusion.
- Risk if not clarified: The submission draft may feel repetitive even though the review artifact is intentionally cautious.
- Freeze-safe? Yes.
- Requires implementation change? No.

## M8 Citation and Artifact Handling

- Issue: Source IDs and repository references need final citation / artifact handling before submission.
- Suggested insertion location: Citation and Artifact Notes.
- Candidate wording: Source IDs should be converted into final bibliography entries only after manual source verification. Repository references should be handled as artifact citations, appendix references, or supplementary material links depending on the target venue.
- Risk if not clarified: Reviewers may see placeholders as unfinished citation practice rather than deliberate draft markers.
- Freeze-safe? Yes.
- Requires implementation change? No.

## L3 WARN Example

- Issue: WARN semantics could include one extra explanatory example during polishing.
- Suggested insertion location: Evaluation interpretation.
- Candidate wording: For example, a scanner may flag `write_file` as high risk, but if the execution only uses `read_file` and `summarize_text`, the run remains a warning rather than a failure because the risky target was not attempted.
- Risk if not clarified: The WARN state may be less intuitive to readers unfamiliar with the distinction between potential risk and triggered violation.
- Freeze-safe? Yes.
- Requires implementation change? No.

## L4 Shorten FDO/data-space Discussion

- Issue: FDO/data-space discussion could be shortened during polishing.
- Suggested insertion location: Discussion.
- Candidate wording: AEP uses FDO/data-space framing only to shape evidence objects for future preservation and reference. It does not implement registry, connector, or usage-control infrastructure.
- Risk if not clarified: Readers may overemphasize the FDO/data-space framing relative to the evidence-linkage contribution.
- Freeze-safe? Yes.
- Requires implementation change? No.
