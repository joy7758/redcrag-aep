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

## v0.2-alpha OpenTelemetry 风格 trace 到 AEP 自举验证

在没有设计伙伴和真实客户流程的情况下，v0.2-alpha 使用合成 OpenTelemetry（开放遥测标准）风格 trace（追踪记录）做自举验证：把 trace 转成 AEP（Agent Execution Profile，智能体执行证据配置文件）证据包，进行 demo（demonstration，演示）级签名，并用 validator（validator，校验器）检查正确和错误样例。

```bash
python -m redcrag_aep.cli convert-otel fixtures/otel_traces/valid_contract_review_trace.json --out outputs/aep_from_otel_contract_review.json --sign
python -m redcrag_aep.cli selfcheck-otel
python -m unittest discover -s tests
```

这不是完整 OpenTelemetry（开放遥测标准）兼容实现，也不替代真实客户反馈。它只证明 v0.2-alpha 已具备 OpenTelemetry 风格 trace 映射 demo（demonstration，演示）、签名、校验和失败样例自检能力。

新增文档：

- `docs/opentelemetry_to_aep_mapping_cn.md`
- `docs/self_validation_without_design_partner_cn.md`
- `docs/public_release_checklist_cn.md`
- `docs/agent_retrieval_card_cn.md`

## v0.2-alpha public-ready 公开准备材料

- `docs/public_repository_readiness_cn.md`
- `docs/technical_blog_draft_v0_2_cn.md`
- `docs/platform_reader_quickstart_cn.md`
- `docs/langfuse_adapter_plan_cn.md`
- `docs/cozeloop_adapter_plan_cn.md`
- `docs/release_announcement_draft_cn.md`
- `llms.txt`
- `ai-index.json`

这些文件用于公开仓库、技术博客、平台方阅读和智能体检索，不改变核心代码功能。
