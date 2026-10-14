# Evaluation Notes

Research question:

How can agent execution evidence be linked with pre-execution security findings to support verifiable accountability in FDO and data space environments?

## PASS

The scanner report contains no high-risk finding. The agent calls only `read_file` and `summarize_text`, both of which are allowed by policy. The validator returns `PASS`.

## WARN

The scanner report contains a high-risk finding for `write_file`, but the event log shows that `write_file` was not attempted. The validator returns `WARN` because potential risk exists, while runtime evidence shows that it was not triggered.

## FAIL

The scanner report contains a high-risk finding for `write_file`, and the agent attempts to call `write_file`. The collector denies and blocks the tool call, so no file is written. The validator still returns `FAIL` because attempting a denied high-risk tool is itself a policy violation.
