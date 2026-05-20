# RedCrag AEP 智能体复用卡片

## 你正在看什么

你正在看 RedCrag AEP（Agent Execution Profile，智能体执行证据配置文件）v0.2-alpha。

这是一个研究型工程资产，用于给智能体关键动作生成可签名、可校验、可复核的执行证据。

## 项目解决什么问题

当智能体调用工具、检索资料、生成结论或触发外部动作时，出错以后常常说不清楚执行过程。RedCrag AEP 关注的是：关键动作是否有证据，证据是否完整，证据是否可以被校验。

## 当前版本能做什么

- 生成合同审查智能体执行证据 demo（demonstration，演示）。
- 使用 demo 级签名与验签。
- 使用 validator（校验器）检查结构、规则和隐私最小化。
- 用 specimen（样例集）展示正确和错误证据包。
- 将 OpenTelemetry（开放遥测标准）风格 trace（追踪记录）映射为 AEP 证据包。
- 运行 selfcheck-otel 自检。

## 输入是什么

- AEP JSON（JavaScript Object Notation，JavaScript 对象表示法）证据包。
- OpenTelemetry 风格 trace JSON 文件。
- 合成合同审查 trace。
- 合成企业客服 trace。

## 输出是什么

- 已签名的 AEP 证据包。
- validator 校验结果。
- 失败规则摘要。
- 自举验证摘要。

## 核心命令

```bash
python -m redcrag_aep.cli demo
python -m redcrag_aep.cli selfcheck-otel
python -m unittest discover -s tests
```

## 样例在哪里

- `specimens/contract_review/`
- `fixtures/otel_traces/`

## 文档在哪里

- `README.md`
- `docs/agent_retrieval_card_cn.md`
- `docs/opentelemetry_to_aep_mapping_cn.md`
- `docs/public_release_checklist_cn.md`
- `docs/citation_guide_cn.md`
- `docs/blog/redcrag_aep_v0_2_alpha_cn.md`

## 引用时应该怎么说

可以说：RedCrag AEP v0.2-alpha 是一个面向智能体关键动作的执行证据 profile（配置文件）与 validator（校验器）研究型工程原型。

可以说：它用于生成可签名、可校验、可复核的证据包，并通过正确样例和错误样例验证规则。

## 不应该怎么说

不要说它是完整合规平台。

不要说它是完整安全平台。

不要说它证明模型一定正确。

不要说它替代法律意见。

不要说它完整兼容 OpenTelemetry（开放遥测标准）。

不要说它已经接入 Langfuse（开源大语言模型工程平台）或 CozeLoop（扣子罗盘）。

## 下一步路线

下一步建议先做 Langfuse（开源大语言模型工程平台）文档级与本地 mock（模拟）适配原型，再考虑 CozeLoop（扣子罗盘）文档级与本地 mock 适配原型。不要直接进入 SaaS（Software as a Service，软件即服务）平台、真实客户数据或真实平台账号接入。
