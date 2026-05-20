# RedCrag AEP 公开仓库准备检查说明

## 1. 当前项目一句话

RedCrag AEP（Agent Execution Profile，智能体执行证据配置文件）给智能体关键动作生成可签名、可校验、可复核的执行证据。

## 2. 当前能公开展示什么

当前可以公开展示：

- AEP（Agent Execution Profile，智能体执行证据配置文件）最小字段。
- demo（demonstration，演示）级签名与验签。
- validator（validator，校验器）规则校验。
- 合同审查 specimen（specimen，样例集）。
- OpenTelemetry（开放遥测标准）风格 trace（追踪记录）到 AEP 的本地映射 demo（demonstration，演示）。
- selfcheck-otel 自检命令。
- 文档级 Langfuse（开源大语言模型工程平台）和 CozeLoop（扣子罗盘）适配计划。

## 3. 当前不能公开声称什么

当前不能公开声称：

- 已经保证合规。
- 已经保证安全。
- 已经证明模型输出正确。
- 已经接入真实客户。
- 已经接入真实 Langfuse（开源大语言模型工程平台）或 CozeLoop（扣子罗盘）。
- 已经完整兼容 OpenTelemetry（开放遥测标准）。
- demo（demonstration，演示）级签名是生产级法律签名。
- RedCrag 是通用 SaaS（Software as a Service，软件即服务）平台。

## 4. 公开前必须确认的 10 项

- [ ] 无真实客户数据。
- [ ] 无合同全文。
- [ ] 无密钥。
- [ ] 无云账号。
- [ ] demo（demonstration，演示）通过。
- [ ] selfcheck-otel 通过。
- [ ] unittest（Python 标准库测试框架）通过。
- [ ] README（项目说明文件）清楚。
- [ ] 边界声明清楚。
- [ ] 没有虚构平台合作。

## 5. 为什么没有真实客户数据

RedCrag AEP 当前处在 v0.2-alpha 自举验证阶段。没有设计伙伴和真实客户流程时，使用合成 trace（追踪记录）样例更安全，也更容易公开复现。真实客户数据会带来隐私、授权、合规和责任边界问题，不适合进入公开仓库。

## 6. 为什么不保存合同全文

AEP（Agent Execution Profile，智能体执行证据配置文件）是执行证据层，不应变成另一个敏感原文仓库。合同全文应保留在客户或平台自己的受控系统里。RedCrag AEP 只保存摘要、引用、来源位置和 SHA-256（Secure Hash Algorithm 256-bit，安全哈希算法 256 位）哈希等最小证据。

## 7. 为什么 demo 级签名不是生产级签名

当前签名是 HMAC-SHA256-DEMO（Hash-based Message Authentication Code with Secure Hash Algorithm 256-bit demonstration，基于安全哈希算法 256 位的演示级消息认证码），用于说明证据包可以签名和验签。它不是生产级公私钥签名，不是法律签名，也没有接入企业密钥体系。

生产环境需要重新评估 Sigstore（开源签名与透明日志项目）、Cosign（签名工具）或企业 KMS（Key Management Service，密钥管理服务）。

## 8. 为什么 OpenTelemetry 只是风格映射

当前转换器处理的是本地 JSON（JavaScript Object Notation，JavaScript 对象表示法）中的 OpenTelemetry（开放遥测标准）风格字段，例如 trace（追踪记录）、span（跨度记录）和 attributes（属性）。它没有实现 OTLP（OpenTelemetry Protocol，开放遥测协议）、资源语义、采样、导出器或完整 SDK（Software Development Kit，软件开发工具包）。

因此只能称为 OpenTelemetry 风格 trace 映射 demo（demonstration，演示），不能称为完整兼容实现。

## 9. 公开仓库建议说明

公开仓库时，README（项目说明文件）应把项目定义为研究型工程原型，而不是产品终版。建议明确写出：

- 当前是 v0.2-alpha。
- 当前没有真实客户数据。
- 当前没有平台合作。
- 当前只提供本地 demo（demonstration，演示）和自检。
- 当前不替代法律意见。

## 10. 后续路线

后续路线建议：

1. 公开仓库并收集技术反馈。
2. 准备技术博客说明 AEP（Agent Execution Profile，智能体执行证据配置文件）和 OpenTelemetry（开放遥测标准）风格映射。
3. 再决定优先做 Langfuse（开源大语言模型工程平台）还是 CozeLoop（扣子罗盘）文档级适配原型。
