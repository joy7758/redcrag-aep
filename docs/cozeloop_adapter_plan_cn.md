# CozeLoop 文档级适配计划

## 1. 为什么考虑 CozeLoop

CozeLoop（扣子罗盘）面向大模型应用开发、调试、观测和评估，适合国内平台嵌入叙事。RedCrag AEP（Agent Execution Profile，智能体执行证据配置文件）可以作为证据层思路，帮助平台方理解关键动作证据如何生成和校验。

当前只是计划，不写真实适配代码。

## 2. RedCrag 与 CozeLoop 的关系

RedCrag 不替代 CozeLoop（扣子罗盘）。CozeLoop 可以继续负责模型应用开发和观测，RedCrag 只把关键动作整理为可签名、可校验、可复核的 AEP 证据包。

## 3. 可能的数据流

可能的数据流：

1. CozeLoop（扣子罗盘）或相关平台导出 trace（追踪记录）或 OpenTelemetry（开放遥测标准）风格数据。
2. RedCrag 本地读取脱敏样例。
3. 映射为 AEP（Agent Execution Profile，智能体执行证据配置文件）。
4. 生成 demo（demonstration，演示）级签名。
5. 运行 validator（validator，校验器）。
6. 输出 gap report（gap report，差距报告）。

## 4. 如何从 trace 或 OpenTelemetry 风格数据生成 AEP

最小映射包括：

- trace id（trace identifier，追踪标识）到 `run_id`。
- tool span（tool span，工具跨度记录）到 `tool_calls`。
- risk level（risk level，风险等级）到工具调用风险字段。
- receipt id（receipt identifier，回执标识）到 `receipt_refs`。
- human review（human review，人工审核）到 `human_review`。
- output summary（output summary，输出摘要）和 source location（source location，来源位置）到 `output_refs`。

## 5. 如何保留 receipt

receipt（receipt，回执）应保留为引用，而不是复制外部系统原始记录。字段可以包括：

- receipt id（receipt identifier，回执标识）。
- 对应 tool call id（tool call identifier，工具调用标识）。
- 回执类型。
- 简短摘要。
- 时间。

## 6. 如何处理 human_review

human_review（human review，人工审核）应表示审核状态，而不是保存完整审核聊天记录。字段可以包括：

- 是否 approved（approved，已批准）。
- 审核人或审核机制引用。
- 审核时间。
- 对应工具调用标识。

高风险动作没有 human_review 时，validator（validator，校验器）应失败。

## 7. 如何避免保存敏感原文

适配原型应避免保存：

- 合同全文。
- 提示词全文。
- 客户完整个人信息。
- API key（Application Programming Interface key，应用程序接口密钥）。
- 私钥或云凭据。

需要保存时，只保存摘要、引用、来源位置和 SHA-256（Secure Hash Algorithm 256-bit，安全哈希算法 256 位）哈希。

## 8. 最小适配原型验收标准

- 使用脱敏 CozeLoop（扣子罗盘）风格或 OpenTelemetry（开放遥测标准）风格样例。
- 能生成 AEP（Agent Execution Profile，智能体执行证据配置文件）证据包。
- 能签名和验签。
- 能运行 validator（validator，校验器）。
- 正确样例通过。
- 错误样例失败。
- 不保存敏感原文。

## 9. 当前不做什么

当前不做：

- 真实 CozeLoop（扣子罗盘）接入。
- 真实生产数据处理。
- 云账号接入。
- 平台合作声明。
- SaaS（Software as a Service，软件即服务）。
- 生产级签名。

## 10. 风险

主要风险：

- 平台实际导出字段未知。
- trace（追踪记录）里可能混入敏感原文。
- receipt（receipt，回执）和 human_review（human review，人工审核）在不同平台表达不同。
- 文档级计划容易被误读为已完成接入。

因此公开表达必须写清楚：当前没有接入真实 CozeLoop（扣子罗盘），只是文档级计划，不宣称平台合作。
