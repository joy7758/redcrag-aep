# RedCrag AEP v0.2-alpha 发布短文草稿

## 1. 发布什么

RedCrag AEP（Agent Execution Profile，智能体执行证据配置文件）v0.2-alpha 是一个给智能体关键动作生成可签名、可校验、可复核执行证据的最小工程原型。

## 2. 为什么做

智能体开始调用工具、触发审批、生成风险意见后，单纯日志很难说明关键动作是否有回执、是否有人审、证据是否被改、是否泄露敏感原文。RedCrag AEP 想把这些问题转成可运行的证据包和校验规则。

## 3. 当前能跑什么

当前仓库可以运行合同审查 demo（demonstration，演示），也可以把 OpenTelemetry（开放遥测标准）风格 trace（追踪记录）转换成 AEP 证据包。正确样例会通过，缺回执、缺人审、泄露合同全文的样例会失败。

## 4. 怎样验证

```bash
python -m redcrag_aep.cli demo
python -m redcrag_aep.cli selfcheck-otel
python -m unittest discover -s tests
```

也可以运行：

```bash
python -m redcrag_aep.cli convert-otel fixtures/otel_traces/valid_contract_review_trace.json --out outputs/aep_from_otel_contract_review.json --sign
```

## 5. 当前边界

这是自举验证，不是商业化产品。当前没有客户数据，没有真实平台账号，没有完整 OpenTelemetry（开放遥测标准）兼容，没有生产级法律签名，也没有接入 Langfuse（开源大语言模型工程平台）或 CozeLoop（扣子罗盘）。

RedCrag AEP 不证明模型一定正确，不替代法律意见，也不保证合规或安全。

## 6. 下一步

下一步会优先准备公开样例库和平台接头说明，再考虑 Langfuse（开源大语言模型工程平台）或 CozeLoop（扣子罗盘）的文档级适配原型。当前阶段不做 SaaS（Software as a Service，软件即服务），不接真实客户数据。
