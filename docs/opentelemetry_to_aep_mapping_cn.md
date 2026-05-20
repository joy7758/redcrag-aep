# OpenTelemetry 风格 trace 到 AEP 映射说明

## 1. 为什么做 OpenTelemetry 到 AEP

OpenTelemetry（开放遥测标准）已经是很多平台和工程系统理解 trace（追踪记录）、span（跨度记录）和 attributes（属性）的通用方式。RedCrag AEP（Agent Execution Profile，智能体执行证据配置文件）需要证明自己不只是一个孤立 demo（demonstration，演示），而是可以从已有执行轨迹里生成可签名、可校验、可复核的证据包。

v0.2-alpha 选择 OpenTelemetry 风格 trace（追踪记录）作为自举验证入口，是因为它不依赖真实客户、不依赖特定平台账号，也不要求先做 SaaS（Software as a Service，软件即服务）。

## 2. 当前 v0.2-alpha 支持什么

当前支持一个最小 OpenTelemetry 风格映射 demo（demonstration，演示）：

- 读取本地 JSON（JavaScript Object Notation，JavaScript 对象表示法）trace（追踪记录）。
- 将 `trace_id` 映射为 AEP（Agent Execution Profile，智能体执行证据配置文件）的 `run_id`。
- 将 `workflow`、`actor`、`task` 映射到 AEP 顶层字段。
- 将名称以 `tool.` 开头或包含 `tool.name` 属性的 span（跨度记录）映射为 `tool_calls`。
- 将 `receipt_id` 或 `tool.receipt_id` 映射为 `receipt_refs`。
- 将 `human_review.approved` 映射为 `human_review`。
- 将 `source_clause_ref` 或 `source_location` 映射为 `output_refs` 来源字段。
- 将 `input.ref`、`output.ref`、`output.summary` 转成引用并生成 SHA-256（Secure Hash Algorithm 256-bit，安全哈希算法 256 位）哈希。
- 将 `full_contract_text` 等敏感字段保留到转换结果中，让 validator（validator，校验器）可以发现隐私风险。

## 3. 当前 v0.2-alpha 不支持什么

当前不支持：

- 完整 OpenTelemetry（开放遥测标准）语义规范。
- OTLP（OpenTelemetry Protocol，开放遥测协议）网络接入。
- Langfuse（开源大语言模型工程平台）真实导出。
- CozeLoop（扣子罗盘）真实导出。
- Phoenix（开源人工智能可观测性平台）真实导出。
- 生产级签名。
- 真实客户数据。
- 平台账号、云账号或密钥接入。

## 4. 字段映射表

| OpenTelemetry 风格字段 | AEP 字段 | 说明 |
| --- | --- | --- |
| `trace_id` | `run_id` | 一次执行的运行标识。 |
| `workflow` | `workflow` | 工作流名称。 |
| `actor` | `actor` | 执行主体，可以是对象或字符串。 |
| `task` | `task` | 任务说明。 |
| `spans[].start_time` | `started_at` / `tool_calls[].started_at` | 顶层取最早开始时间；工具调用取 span 自身时间。 |
| `spans[].end_time` | `completed_at` / `tool_calls[].completed_at` | 顶层取最晚结束时间；工具调用取 span 自身时间。 |
| `spans[].name` | `tool_calls[].tool_name` | 名称以 `tool.` 开头时映射为工具调用。 |
| `attributes["tool.name"]` | `tool_calls[].tool_name` | 显式工具名优先。 |
| `attributes["tool.purpose"]` | `tool_calls[].purpose` | 工具调用目的。 |
| `attributes["tool.risk_level"]` / `attributes["risk_level"]` | `tool_calls[].risk_level` | 风险等级。 |
| `attributes["tool.requires_receipt"]` / `attributes["requires_receipt"]` | `tool_calls[].requires_receipt` | 是否需要回执。 |
| `attributes["tool.receipt_id"]` / `attributes["receipt_id"]` | `receipt_refs[]` | 外部动作回执引用。 |
| `attributes["human_review.approved"]` | `human_review.approved` | 是否有人工审核或二次确认。 |
| `attributes["human_review.reviewer"]` | `human_review.reviewers[]` | 审核人或审核机制标识。 |
| `attributes["source_clause_ref"]` | `output_refs[].source_clause_ref` | 合同条款来源引用。 |
| `attributes["source_location"]` | `output_refs[].source_location` | 来源位置。 |
| `attributes["input.ref"]` | `input_refs[]` | 输入引用，不保存敏感原文。 |
| `attributes["output.ref"]` | `output_refs[].ref` | 输出引用。 |
| `attributes["output.summary"]` | `output_refs[].summary` | 输出摘要。 |
| `attributes["full_contract_text"]` | `metadata.sensitive_trace_attributes[]` | 故意保留，供 validator 发现隐私风险。 |

## 5. 隐私边界

AEP（Agent Execution Profile，智能体执行证据配置文件）不应成为敏感原文仓库。当前映射优先保存引用、摘要、来源位置和哈希。

如果 trace（追踪记录）中出现 `full_contract_text`、`raw_medical_record`、`customer_secret`、`private_key` 或 `api_key` 等字段，转换器不会静默丢弃，而是保留到 `metadata.sensitive_trace_attributes` 中。这样 validator（validator，校验器）可以明确失败，提醒这类字段不应进入证据包。

## 6. 与 Langfuse / CozeLoop / Phoenix 的关系

Langfuse（开源大语言模型工程平台）、CozeLoop（扣子罗盘）和 Phoenix（开源人工智能可观测性平台）都可以被理解为潜在 trace（追踪记录）来源或观测系统来源。

当前 v0.2-alpha 没有接入这些平台，也没有声称完成适配。它只说明：如果平台能导出类似 OpenTelemetry 风格的 trace（追踪记录），RedCrag 可以把其中的关键动作映射为 AEP（Agent Execution Profile，智能体执行证据配置文件）证据包。

## 7. 为什么这不是完整 OpenTelemetry 实现

完整 OpenTelemetry（开放遥测标准）涉及正式语义约定、OTLP（OpenTelemetry Protocol，开放遥测协议）、资源信息、上下文传播、采样、导出器和多语言 SDK（Software Development Kit，软件开发工具包）。

v0.2-alpha 只处理本地 JSON（JavaScript Object Notation，JavaScript 对象表示法）中的少量字段，目标是验证 AEP 证据映射，不是实现完整遥测系统。

## 8. 下一步如何做真实平台接头

下一步可以按低风险顺序推进：

1. 做 Langfuse（开源大语言模型工程平台）导出样例到 AEP 的本地 mock（mock，模拟）适配。
2. 做 CozeLoop（扣子罗盘）导出样例到 AEP 的本地 mock（mock，模拟）适配。
3. 再决定是否做真实平台导出器或 SDK（Software Development Kit，软件开发工具包）接口。

在真实接头前，仍然不接客户数据、不接生产密钥、不承诺完整平台兼容。
