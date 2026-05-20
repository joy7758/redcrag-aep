# RedCrag AEP 3 分钟演示脚本

## 0:00 - 0:30 开场

RedCrag 给智能体关键动作生成可签名、可校验、可复核的执行证据。本 demo 使用合同审查场景，但不保存合同全文，只保存条款引用、摘要、哈希、回执和人审状态。

## 0:30 - 1:10 运行 demo

```bash
python -m redcrag_aep.cli demo
```

说明输出里的 `validation_passed: true`，并指出 demo 会生成 `outputs/redcrag_aep_contract_review_demo_bundle.json`。

## 1:10 - 1:40 展示有效样例

打开 `specimens/contract_review/valid_bundle.json`，说明它包含最小 AEP 字段、3 个 tool call、1 个 receipt、approved human review、source_clause_ref、content_hashes 和 demo signature。

## 1:40 - 2:10 展示 validator 通过

```bash
python -m redcrag_aep.cli validate specimens/contract_review/valid_bundle.json
```

说明 validator（校验器）检查结构、规则、隐私最小化、content hash 和 demo 签名。

## 2:10 - 2:35 展示错误样例失败

```bash
python -m redcrag_aep.cli validate specimens/contract_review/invalid_missing_human_review.json
```

指出 high-risk tool call 缺少 approved human review，因此失败是预期结果。

## 2:35 - 3:00 说明证明边界

能证明：记录结构完整、demo 签名未被改、关键动作是否有回执、是否有人审、是否满足规则。

不能证明：模型一定正确、外部世界事实一定真实、系统已经完整合规、法律责任自动免除。
