# RedCrag AEP 平台方快速阅读指南

## 1. RedCrag 不替代平台

RedCrag AEP（Agent Execution Profile，智能体执行证据配置文件）不替代现有智能体平台、观测平台、评测平台或行业系统。平台仍负责模型调用、智能体编排、工具执行、权限、日志和业务流程。

RedCrag 只关注关键动作证据层。

## 2. RedCrag 是证据层

证据层回答的问题是：

- 关键动作是什么。
- 是否需要 receipt（receipt，回执）。
- 是否需要 human review（human review，人工审核）。
- 输出结论是否有来源引用。
- 证据包是否被改过。
- 是否保存了不该保存的敏感原文。

## 3. 平台已有 trace 时，RedCrag 做什么

如果平台已有 trace（追踪记录），RedCrag 可以把其中的关键 span（跨度记录）映射为 AEP（Agent Execution Profile，智能体执行证据配置文件）字段。v0.2-alpha 已提供 OpenTelemetry（开放遥测标准）风格 trace 到 AEP 的本地映射 demo（demonstration，演示）。

## 4. 平台已有评测时，RedCrag 做什么

如果平台已有评测，RedCrag 不替代评测指标。RedCrag 可以补充执行证据：评测结果来自哪次运行，关键工具调用是否有回执，高风险结论是否有人审。

## 5. 平台已有日志时，RedCrag 做什么

如果平台已有日志，RedCrag 不要求复制全部日志。RedCrag 只提取可复核字段，例如工具名称、目的、风险等级、回执标识、人工审核状态、来源引用和内容哈希。

## 6. 三种未来接入方式

### OpenTelemetry 导出

OpenTelemetry（开放遥测标准）导出适合已有 trace（追踪记录）系统的平台。下一步可以做导出样例到 AEP（Agent Execution Profile，智能体执行证据配置文件）的适配原型。

### MCP 工具插件

MCP（Model Context Protocol，模型上下文协议）工具插件适合在工具调用边界直接生成 receipt（receipt，回执）、risk level（risk level，风险等级）和 human review（human review，人工审核）字段。

### SDK / OEM

SDK（Software Development Kit，软件开发工具包）/OEM（Original Equipment Manufacturer，原厂嵌入）适合行业解决方案商，把 AEP 生成、签名和 validator（validator，校验器）嵌入已有产品流程。

## 7. 当前 v0.2-alpha 已经完成什么

- AEP（Agent Execution Profile，智能体执行证据配置文件）最小证据包。
- demo（demonstration，演示）级签名。
- validator（validator，校验器）。
- 合同审查样例。
- OpenTelemetry（开放遥测标准）风格 trace（追踪记录）映射 demo（demonstration，演示）。
- selfcheck-otel 自检。
- 公开阅读和检索材料。

## 8. 当前 v0.2-alpha 还没完成什么

- 没有完整 OpenTelemetry（开放遥测标准）兼容。
- 没有真实 Langfuse（开源大语言模型工程平台）接入。
- 没有真实 CozeLoop（扣子罗盘）接入。
- 没有生产级签名。
- 没有真实客户数据。
- 没有 SaaS（Software as a Service，软件即服务）平台。

## 9. 平台方最可能关心的 5 个问题

1. 会不会要求上传敏感原文？
2. 会不会替代现有平台能力？
3. 能否从已有 trace（追踪记录）或日志中提取？
4. 高风险动作、人审和回执如何表示？
5. 当前是否已经可用于生产？

当前回答是：不上传敏感原文，不替代平台，只做本地映射 demo（demonstration，演示），生产使用还需要真实适配和签名体系。

## 10. 合作前要确认的边界

合作前至少确认：

- 数据是否脱敏。
- 是否禁止保存提示词全文、合同全文或客户个人信息。
- trace（追踪记录）字段能否导出。
- 哪些动作算高风险。
- 哪些动作需要 receipt（receipt，回执）。
- 哪些动作需要 human review（human review，人工审核）。
- 是否只是适配原型，不是生产接入。

当前只能说下一步可以做适配原型，不能说已经支持所有平台。
