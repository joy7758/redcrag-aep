# RedCrag AEP v0.1 最小试点包

RedCrag AEP v0.1 是一个合同审查智能体执行证据 demo（演示）。它用于展示如何把智能体关键动作记录成可签名、可校验、可复核的 AEP（Agent Execution Profile，智能体执行证据配置文件）证据包。

## 已完成能力

- AEP（Agent Execution Profile，智能体执行证据配置文件）最小字段。
- demo（演示）级签名。
- validator（校验器）。
- 1 个有效样例。
- 4 个无效样例。
- 合同审查 demo（演示）。
- unittest（Python 标准库测试框架）测试通过。

## 明确未做

- 生产级签名。
- 真实 OpenTelemetry（开放遥测标准）全量兼容。
- SaaS（Software as a Service，软件即服务）。
- 真实客户数据接入。
- 法律合规结论。

## 版本边界

这份证据包能证明记录结构完整性、demo 签名状态、关键动作回执、人审状态和规则校验结果。它不能证明模型一定正确，不能证明外部世界事实一定真实，也不能自动免除法律责任。
