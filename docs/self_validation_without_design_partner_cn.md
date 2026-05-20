# 没有设计伙伴时的自举验证路线

## 1. 为什么可以暂时跳过人工反馈

RedCrag AEP（Agent Execution Profile，智能体执行证据配置文件）v0.1 已经完成工程包和对外材料，但当前没有设计伙伴、没有客户团队、没有真实业务流程。继续等待人工反馈会让项目停住。

因此 v0.2-alpha 选择自举验证：用合成 OpenTelemetry（开放遥测标准）风格 trace（追踪记录）证明项目可以接入已有执行轨迹、生成 AEP 证据包、签名、校验并发现问题。

## 2. 跳过人工反馈的风险

跳过人工反馈有明显风险：

- 合成样例可能低估真实流程复杂度。
- 真实平台导出的字段可能与样例不同。
- 客户真正关心的回执、人审和复盘边界可能不一样。
- 当前规则可能覆盖不到真实业务风险。
- 文档表达可能还没有经过真实买方或平台方验证。

所以自举验证不能替代真实客户反馈。

## 3. 用什么替代人工反馈

当前阶段用三类资产临时代替人工反馈：

- 合成 trace（追踪记录）样例。
- 自动 selfcheck（self-check，自检）命令。
- 明确的失败样例，包括缺回执、缺人工审核和敏感信息泄露。

它们不能证明市场需求，但能证明技术路径不是空话。

## 4. 合成 trace 样例的意义

合成 trace（追踪记录）样例让仓库自己可以说明：

- 正常合同审查 trace（追踪记录）可以转成 AEP（Agent Execution Profile，智能体执行证据配置文件）。
- 缺 receipt（receipt，回执）会失败。
- 缺 human review（human review，人工审核）会失败。
- 泄露 full contract text（full contract text，合同全文）会失败。
- 企业客服退款场景也能用同一套证据思路表达。

这比只保留一个静态 demo（demonstration，演示）更接近平台接头方向。

## 5. 自检命令如何运行

运行：

```bash
python -m redcrag_aep.cli selfcheck-otel
```

预期结果：

- `valid_contract_review_trace.json` 通过。
- `invalid_missing_receipt_trace.json` 失败。
- `invalid_missing_human_review_trace.json` 失败。
- `invalid_full_contract_leak_trace.json` 失败。
- `valid_customer_service_trace.json` 通过。
- `overall_passed` 为 `true`。

## 6. 怎样判断项目是否继续推进

如果以下条件成立，项目可以继续推进：

- demo（demonstration，演示）仍然通过。
- unittest（Python 标准库测试框架）仍然通过。
- selfcheck-otel 自检通过。
- 失败样例能解释清楚。
- 新增文档没有夸大合规、安全、模型正确性或平台合作。

如果这些条件不成立，应先修复证据模型和说明边界，不应继续扩功能。

## 7. 什么时候必须重新找真人反馈

以下情况必须重新找真人反馈：

- 准备接真实平台导出数据。
- 准备定义行业高风险动作。
- 准备进入合同审查、客服、医疗、金融等具体业务场景。
- 准备公开声称某个平台适配可用。
- 准备从 demo（demonstration，演示）级签名转向生产级签名。

真实反馈迟早需要，只是当前阶段可以延后。
