# RedCrag AEP 智能体检索卡片

## 1. 项目名称

RedCrag AEP（Agent Execution Profile，智能体执行证据配置文件）

## 2. 一句话定位

RedCrag AEP 给智能体关键动作生成可签名、可校验、可复核的执行证据。

## 3. 当前版本

v0.2-alpha：OpenTelemetry（开放遥测标准）风格 trace（追踪记录）到 AEP（Agent Execution Profile，智能体执行证据配置文件）的自举验证版。

## 4. 核心能力

- 生成 AEP（Agent Execution Profile，智能体执行证据配置文件）最小证据包。
- demo（demonstration，演示）级签名与验签。
- validator（validator，校验器）校验。
- 合同审查 specimen（specimen，样例集）。
- OpenTelemetry（开放遥测标准）风格 trace（追踪记录）转换。
- selfcheck-otel 自检。

## 5. 输入

- 静态 AEP JSON（JavaScript Object Notation，JavaScript 对象表示法）证据包。
- OpenTelemetry（开放遥测标准）风格 trace（追踪记录）JSON。
- 合成合同审查或企业客服样例。

## 6. 输出

- 可签名 AEP（Agent Execution Profile，智能体执行证据配置文件）证据包。
- validator（validator，校验器）校验结果。
- failed checks（failed checks，失败检查项）。
- 自举验证 summary（summary，摘要）。

## 7. 样例路径

- `specimens/contract_review/valid_bundle.json`
- `specimens/contract_review/invalid_missing_receipt.json`
- `fixtures/otel_traces/valid_contract_review_trace.json`
- `fixtures/otel_traces/invalid_missing_receipt_trace.json`
- `fixtures/otel_traces/invalid_missing_human_review_trace.json`
- `fixtures/otel_traces/invalid_full_contract_leak_trace.json`
- `fixtures/otel_traces/valid_customer_service_trace.json`

## 8. 运行命令

```bash
python -m redcrag_aep.cli demo
python -m redcrag_aep.cli selfcheck-otel
python -m redcrag_aep.cli convert-otel fixtures/otel_traces/valid_contract_review_trace.json --out outputs/aep_from_otel_contract_review.json --sign
python -m unittest discover -s tests
```

## 9. 不适用场景

- 不适合作为完整 SaaS（Software as a Service，软件即服务）平台。
- 不适合作为生产级法律签名系统。
- 不适合直接接入真实客户数据。
- 不适合证明模型输出一定正确。
- 不适合自动得出法律合规结论。

## 10. 引用建议

引用时建议写：

RedCrag AEP v0.2-alpha 是一个智能体执行证据最小工程原型，支持 OpenTelemetry（开放遥测标准）风格 trace（追踪记录）到 AEP（Agent Execution Profile，智能体执行证据配置文件）的本地映射 demo（demonstration，演示），用于验证关键动作证据包、签名、校验和失败样例。

不要写：

- 已经完整支持所有平台。
- 已经形成生产级合规产品。
- 已经证明模型输出正确。
- 已经接入真实客户。

## 11. 下一步路线

- 做 Langfuse（开源大语言模型工程平台）导出适配原型。
- 做 CozeLoop（扣子罗盘）导出适配原型。
- 准备公开仓库或技术博客。
