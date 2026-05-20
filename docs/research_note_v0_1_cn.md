# RedCrag AEP v0.1 研究记录

## 1. 研究问题

当前研究问题是：智能体执行过程中的关键动作，能否形成可签名、可校验、可复核的证据记录。

这个问题不同于“模型输出是否一定正确”。v0.1 关注的是执行证据，而不是直接判断模型答案的真伪。

## 2. v0.1 最小假设

v0.1 的最小假设包括：

- 智能体一次运行可以被整理为 AEP（Agent Execution Profile，智能体执行证据配置文件）证据包。
- 关键工具调用可以记录 purpose（purpose，目的）、risk level（risk level，风险等级）、receipt（receipt，回执）和 human review（human review，人工审核）状态。
- 合同审查结论可以引用 source clause reference（source clause reference，来源条款引用），而不是保存合同全文。
- validator（validator，校验器）可以检查结构、规则、隐私最小化、内容哈希和签名状态。
- specimen（specimen，样例集）可以同时包含正确样例和错误样例，用于证明规则有效。

## 3. AEP 字段边界

AEP（Agent Execution Profile，智能体执行证据配置文件）当前是 profile（profile，配置文件），不是正式标准。

v0.1 字段边界包括：

- `schema_version`：配置文件版本。
- `run_id`：运行标识。
- `workflow`：工作流。
- `actor`：执行主体。
- `task`：任务说明。
- `started_at` 和 `completed_at`：运行时间边界。
- `tool_calls`：工具调用记录。
- `input_refs`：输入引用，不保存敏感原文。
- `output_refs`：输出引用和来源位置。
- `receipt_refs`：外部动作回执。
- `human_review`：人工审核记录。
- `policy_results`：策略检查结果。
- `content_hashes`：SHA-256（Secure Hash Algorithm 256-bit，安全哈希算法 256 位）内容哈希。
- `signature`：demo（demonstration，演示）级签名。
- `metadata`：非敏感元数据。

## 4. validator 设计原则

validator（validator，校验器）遵循几个原则：

- 先验证最小结构是否完整。
- 再验证关键策略，例如高风险动作必须有人审。
- 再验证外部动作是否有回执。
- 再验证合同审查结论是否有来源引用。
- 再验证隐私最小化边界，例如不允许 full contract text（full contract text，合同全文）字段。
- 最后验证 content hash（content hash，内容哈希）和 demo（demonstration，演示）级签名。

validator（validator，校验器）的目标不是判断模型是否正确，而是判断证据记录是否满足可复查规则。

## 5. specimen 意义

specimen（specimen，样例集）的意义在于让规则可以被反复验证。

v0.1 包含：

- 一个正确样例。
- 一个缺 receipt（receipt，回执）的错误样例。
- 一个缺 human review（human review，人工审核）的错误样例。
- 一个 content hash（content hash，内容哈希）不匹配的错误样例。
- 一个包含 full contract text（full contract text，合同全文）的错误样例。

这些样例证明：规则不是文档描述，而是可以运行、可以失败、可以回归测试。

## 6. 当前不能证明什么

v0.1 不能证明：

- 模型输出一定正确。
- 外部事实一定真实。
- 系统一定合规。
- 法律责任自动免除。
- demo（demonstration，演示）级签名等同于生产级法律签名。
- AEP（Agent Execution Profile，智能体执行证据配置文件）已经成为正式标准。

## 7. 下一步研究问题

下一步研究问题包括：

- OpenTelemetry（开放遥测标准） trace（trace，追踪记录）如何稳定映射到 AEP（Agent Execution Profile，智能体执行证据配置文件）。
- MCP（Model Context Protocol，模型上下文协议）工具调用边界如何自动产生 receipt（receipt，回执）和 human review（human review，人工审核）字段。
- 不同行业场景中的高风险动作如何定义。
- 如何从 demo（demonstration，演示）级签名过渡到生产级签名体系。
- 如何把 gap report（gap report，差距报告）转化为客户可执行的治理 backlog（backlog，待办列表）。
