# Langfuse 文档级适配计划

## 1. 为什么先考虑 Langfuse

Langfuse（开源大语言模型工程平台）面向 LLM（Large Language Model，大语言模型）应用观测、trace（追踪记录）和评估。它适合作为国际开源开发者生态中的第一类文档级适配对象。

当前只是计划，不写真实适配代码。

## 2. RedCrag 与 Langfuse 的关系

RedCrag AEP（Agent Execution Profile，智能体执行证据配置文件）不替代 Langfuse。Langfuse 可以记录 LLM 应用 trace（追踪记录）和观测数据；RedCrag 可以把其中的关键动作提取成可签名、可校验、可复核的 AEP 证据包。

## 3. 可能的数据流

可能的数据流：

1. Langfuse 侧导出 trace（追踪记录）或 OpenTelemetry（开放遥测标准）风格数据。
2. RedCrag 本地读取脱敏导出文件。
3. 转换为 AEP（Agent Execution Profile，智能体执行证据配置文件）。
4. 使用 demo（demonstration，演示）级签名。
5. 运行 validator（validator，校验器）。
6. 输出 failed checks（failed checks，失败检查项）和 gap report（gap report，差距报告）。

## 4. 需要从 Langfuse 或 OpenTelemetry 读取什么

最小字段包括：

- trace（追踪记录）标识。
- span（跨度记录）标识。
- 工具调用名称。
- 工具调用目的。
- 风险等级。
- 是否需要 receipt（receipt，回执）。
- receipt id（receipt identifier，回执标识）。
- human review（human review，人工审核）状态。
- 输出摘要。
- 来源引用或来源位置。

不读取真实生产密钥，不读取客户全文，不保存提示词全文和合同全文。

## 5. 如何转成 AEP

转换规则可以沿用 v0.2-alpha：

- trace id 映射为 `run_id`。
- tool span（tool span，工具跨度记录）映射为 `tool_calls`。
- receipt id 映射为 `receipt_refs`。
- human review 字段映射为 `human_review`。
- output summary（output summary，输出摘要）和 source reference（source reference，来源引用）映射为 `output_refs`。
- 引用和摘要生成 SHA-256（Secure Hash Algorithm 256-bit，安全哈希算法 256 位）哈希。

## 6. 如何签名

适配原型阶段继续使用 HMAC-SHA256-DEMO（Hash-based Message Authentication Code with Secure Hash Algorithm 256-bit demonstration，基于安全哈希算法 256 位的演示级消息认证码）。

这不是生产级法律签名。生产阶段需要评估 Sigstore（开源签名与透明日志项目）、Cosign（签名工具）或企业 KMS（Key Management Service，密钥管理服务）。

## 7. 如何运行 validator

转换后运行：

```bash
python -m redcrag_aep.cli validate path/to/aep_bundle.json
```

validator（validator，校验器）检查结构、回执、人审、隐私、哈希和签名状态。

## 8. 适配原型的最小验收标准

- 使用脱敏 Langfuse 风格导出样例。
- 能转换为 AEP（Agent Execution Profile，智能体执行证据配置文件）。
- 能 demo（demonstration，演示）级签名。
- 能通过或按预期失败。
- 能报告 failed checks（failed checks，失败检查项）。
- 不保存提示词全文和合同全文。

## 9. 当前不做什么

当前不做：

- 真实 Langfuse 接入。
- 真实生产数据处理。
- SaaS（Software as a Service，软件即服务）。
- 云账号接入。
- 生产级签名。
- 实时同步。

## 10. 风险

主要风险：

- Langfuse 导出字段与 OpenTelemetry（开放遥测标准）风格样例不一致。
- trace（追踪记录）中可能包含敏感提示词全文。
- 平台评测指标与 AEP 证据规则边界不同。
- 用户可能误以为 demo（demonstration，演示）级签名已经具备法律效力。

因此第一步只做文档级计划和本地 mock（mock，模拟）样例。
