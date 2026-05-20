# RedCrag AEP Demo

RedCrag 给智能体关键动作生成可签名、可校验、可复核的执行证据。

RedCrag gives agent critical actions signable, validatable, and reviewable execution evidence.

## Quick Run

```bash
python -m redcrag_aep.cli demo
python -m unittest discover -s tests
```

If `python` is not available, use `python3`.

## RedCrag AEP Demo

This repository-level demo is a minimal Agent Execution Profile (AEP) trial package for a contract review agent. It includes:

- `redcrag_aep/`: canonical JSON, demo signing, validation, OpenTelemetry-style trace mapping, and CLI.
- `specimens/contract_review/valid_bundle.json`: a passing contract review evidence bundle.
- `specimens/contract_review/invalid_missing_receipt.json`: fails because a receipt-required tool call has no matching receipt.
- `specimens/contract_review/invalid_missing_human_review.json`: fails because a high-risk tool call lacks approved human review.
- `specimens/contract_review/invalid_tampered_hash.json`: fails because a referenced output value no longer matches its SHA-256 hash.
- `specimens/contract_review/invalid_full_contract_leak.json`: fails because raw full contract text is present.

## Boundaries

This is not a general agent platform, not a complete compliance product, not legal advice, and not proof that the model answer is correct. The included HMAC signature is demo-grade only; production signing should use a real key-management and signing system.

这不是通用智能体平台，不是完整合规产品，不替代法律意见，不承诺模型正确。

## Next Steps

- 做真实 OpenTelemetry（开放遥测标准）到 AEP（Agent Execution Profile，智能体执行证据配置文件）的映射。
- 做 CozeLoop（扣子罗盘）或 Langfuse（开源大语言模型工程平台）接头。
- 找合同审查或企业客服智能体做设计伙伴试点。

## v0.1 对外材料

- `docs/public_demo_walkthrough_cn.md`
- `docs/trial_package_for_contract_review_cn.md`
- `docs/platform_embedding_brief_cn.md`
- `docs/design_partner_outreach_cn.md`
- `docs/research_note_v0_1_cn.md`

这些文档用于演示、试点沟通、平台嵌入沟通和研究记录，不改变代码功能。
