# RedCrag AEP v0.1 平台嵌入说明

## 1. RedCrag 不替代平台

RedCrag AEP（Agent Execution Profile，智能体执行证据配置文件）v0.1 不替代现有智能体平台、观测平台、工作流平台或行业解决方案。它不是新的 SaaS（Software as a Service，软件即服务）平台，也不声称已经覆盖所有平台。

RedCrag 关注的是证据层：关键动作如何被记录、签名、校验和复核。

## 2. RedCrag 作为证据层嵌入平台

平台继续负责智能体编排、模型调用、工具调用、用户界面、权限管理和业务流程。RedCrag 只嵌入关键动作证据：

- 哪个智能体在什么任务里调用了什么工具。
- 该工具调用的目的是什么。
- 是否属于高风险动作。
- 是否需要 receipt（receipt，回执）。
- 是否需要 human review（human review，人工审核）。
- 输出结论是否能引用来源位置。
- 证据包是否能被 validator（validator，校验器）检查。

## 3. 三种接入方式

### OpenTelemetry（开放遥测标准）到 AEP（Agent Execution Profile，智能体执行证据配置文件）

平台已有 trace（trace，追踪记录）时，可以把关键 span（span，追踪片段）映射到 AEP（Agent Execution Profile，智能体执行证据配置文件）字段。v0.1 已具备最小证据包和校验能力，下一步可以做真实字段映射。

### MCP（Model Context Protocol，模型上下文协议）工具插件

如果平台通过 MCP（Model Context Protocol，模型上下文协议）管理工具调用，可以在工具插件边界输出 tool call（tool call，工具调用）、risk level（risk level，风险等级）、receipt id（receipt identifier，回执标识）和 human review（human review，人工审核）状态。

### SDK（Software Development Kit，软件开发工具包）/OEM（Original Equipment Manufacturer，原厂嵌入）支持

对于行业平台或企业内部系统，可以通过 SDK（Software Development Kit，软件开发工具包）或 OEM（Original Equipment Manufacturer，原厂嵌入）方式，把 AEP（Agent Execution Profile，智能体执行证据配置文件）生成、签名和校验能力嵌入到现有流程中。

## 4. 适合接入的平台类型

适合进一步讨论的对象包括：

- CozeLoop（扣子罗盘）。
- Langfuse（开源大语言模型工程平台）。
- 云厂商智能体平台。
- 行业解决方案商。

这里不表示已经达成合作，也不表示已经支持所有平台。当前只能说：v0.1 已具备最小证据包和校验能力，下一步可以做接头。

## 5. 平台方为什么会关心

平台方会关心 RedCrag 的原因通常不是“再加一个日志”，而是补上几个责任边界问题：

- 高风险动作是否有人审。
- 外部动作是否有回执。
- 关键输出是否能回到来源引用。
- 证据记录是否被篡改。
- 日志是否泄露敏感原文。
- 出问题后是否能复盘。

这些问题在企业客户、法务流程、客服流程、采购流程和监管敏感流程里会越来越重要。

## 6. 平台方会担心什么

平台方可能会担心：

- RedCrag 是否替代平台能力。
- 是否要求平台上传敏感原文。
- 是否会改变现有智能体编排逻辑。
- 是否要求接入生产密钥。
- 是否会承诺平台无法承诺的法律合规结果。
- 是否增加过重实施成本。

v0.1 的回答是：不替代平台，不保存合同全文，不接生产密钥，不做法律合规结论，只先验证关键动作证据是否能形成、签名、校验和失败。

## 7. 我们的边界

当前边界如下：

- 不虚构已达成合作。
- 不宣称支持所有平台。
- 不做通用 SaaS（Software as a Service，软件即服务）平台。
- 不接真实客户数据。
- 不保存合同全文。
- 不把 demo（demonstration，演示）级签名说成生产级法律签名。
- 只说明 v0.1 已具备最小证据包和校验能力，下一步可以做 OpenTelemetry（开放遥测标准）、MCP（Model Context Protocol，模型上下文协议）或 SDK（Software Development Kit，软件开发工具包）接头。
