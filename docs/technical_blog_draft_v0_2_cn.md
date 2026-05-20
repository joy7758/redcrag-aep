# RedCrag AEP v0.2-alpha：给智能体关键动作生成可验证执行证据

## 1. 问题：智能体做了什么，为什么说不清

智能体越来越多地调用工具、读写系统、触发审批、生成建议。问题是，当结果出错时，很多系统只能看到一段日志或一段聊天记录，很难回答：关键动作是什么，谁批准了，外部系统有没有回执，证据后来有没有被改。

RedCrag AEP（Agent Execution Profile，智能体执行证据配置文件）关注的不是“再做一个智能体平台”，而是把关键执行过程整理成可签名、可校验、可复核的证据包。

## 2. 现有 trace 为什么还不够

trace（追踪记录）能告诉我们系统调用链路，但它通常不直接回答责任边界问题。例如：

- 哪个工具调用是高风险动作。
- 哪个动作必须有 receipt（receipt，回执）。
- 哪个结论必须有人审。
- 哪些输出应该有来源引用。
- 日志里是否错误保存了合同全文。

所以 RedCrag AEP 不是替代 trace，而是在 trace 之上提取执行证据。

## 3. RedCrag AEP 想解决什么

RedCrag AEP 想解决的是智能体关键动作的证据化问题。它把一次执行过程转成 AEP（Agent Execution Profile，智能体执行证据配置文件）证据包，并用 validator（validator，校验器）检查结构、回执、人审、隐私和签名状态。

它不证明模型一定正确，也不替代法律意见。

## 4. v0.1 做了什么

v0.1 做了合同审查智能体执行证据最小试点包：

- AEP 最小字段。
- demo（demonstration，演示）级签名。
- validator（validator，校验器）。
- 一个正确样例。
- 四个错误样例。
- unittest（Python 标准库测试框架）回归测试。

错误样例覆盖缺回执、缺人工审核、证据篡改和合同全文泄露。

## 5. v0.2-alpha 新增了什么

v0.2-alpha 新增了 OpenTelemetry（开放遥测标准）风格 trace（追踪记录）到 AEP 的自举验证：

- 合成 trace（追踪记录）样例。
- trace 到 AEP 的本地转换命令。
- `selfcheck-otel` 自检命令。
- 企业客服退款合成样例。
- 平台接头说明和智能体检索索引。

这一步是自举验证，不能替代真实客户反馈。

## 6. OpenTelemetry 风格 trace 如何映射到 AEP

映射思路很直接：

- `trace_id` 映射为 `run_id`。
- `workflow`、`actor`、`task` 进入 AEP 顶层。
- 名称以 `tool.` 开头的 span（跨度记录）映射为 `tool_calls`。
- `receipt_id` 映射为 `receipt_refs`。
- `human_review.approved` 映射为 `human_review`。
- `source_clause_ref` 或 `source_location` 映射为输出来源。
- `input.ref`、`output.ref`、`output.summary` 生成引用和 SHA-256（Secure Hash Algorithm 256-bit，安全哈希算法 256 位）哈希。

当前只是 OpenTelemetry 风格映射 demo（demonstration，演示），不是完整 OpenTelemetry 兼容实现。

## 7. validator 检查什么

validator（validator，校验器）检查：

- 最小 AEP 字段是否完整。
- 工具调用是否有名称、时间和目的。
- 高风险动作是否有人审。
- 需要回执的动作是否有对应回执。
- 合同审查结论是否有来源条款或来源位置。
- 是否出现合同全文、密钥等敏感字段。
- 内容哈希是否匹配。
- demo（demonstration，演示）级签名是否有效。

## 8. 错误样例为什么重要

只有正确样例不够。错误样例能证明规则会真的失败：

- 缺回执会失败。
- 缺人审会失败。
- 敏感字段泄露会失败。
- 哈希不匹配会失败。

这让 RedCrag AEP 更像一个可验证工程资产，而不是一份说明文档。

## 9. 能证明什么

当前能证明：

- 证据包结构可以被检查。
- demo（demonstration，演示）级签名可以被验证。
- 关键动作回执、人审和来源引用可以被检查。
- OpenTelemetry（开放遥测标准）风格 trace（追踪记录）可以转换成 AEP（Agent Execution Profile，智能体执行证据配置文件）。
- 错误样例会按预期失败。

## 10. 不能证明什么

当前不能证明：

- 模型输出一定正确。
- 系统一定合规。
- 系统一定安全。
- demo（demonstration，演示）级签名是生产级法律签名。
- 已经接入 Langfuse（开源大语言模型工程平台）或 CozeLoop（扣子罗盘）。
- 已经有客户或商业化交付。

## 11. 下一步：平台接头与公开样例库

下一步不是做 SaaS（Software as a Service，软件即服务），而是继续沉淀公开技术资产：

1. 公开仓库。
2. 扩展合成样例库。
3. 做 Langfuse（开源大语言模型工程平台）文档级导出适配原型。
4. 做 CozeLoop（扣子罗盘）文档级导出适配原型。

真实平台账号和真实客户数据应等到边界明确后再考虑。
