# RedCrag AEP v0.2-alpha：给智能体关键动作生成可验证执行证据

## 1. 问题：智能体做了什么，为什么说不清

智能体已经不只是回答问题。它会检索资料、调用工具、生成报告，甚至触发外部系统动作。能力变强以后，一个问题更明显：出错以后，怎样说清楚它做了什么、有没有回执、有没有人工审核、证据后来有没有被改？

普通日志能记录运行，但不一定说明证据是否够用。比如合同审查智能体给出高风险意见，如果没有来源条款、人工审核和回执，事后很难复核。

## 2. RedCrag AEP 是什么

RedCrag AEP（Agent Execution Profile，智能体执行证据配置文件）是一个面向智能体关键动作的执行证据 profile（配置文件）与 validator（校验器）研究型工程原型。它把一次关键执行过程整理成可签名、可校验、可复核的证据包。

它不是智能体平台，不是完整合规产品，也不是普通日志系统。它只做最小证据结构：关键动作、输入输出引用、回执、人工审核、内容哈希、规则结果和 demo（demonstration，演示）级签名。

## 3. v0.1 做了什么

v0.1 先选择合同审查场景做 demo。它提供 AEP 最小字段、demo 级签名与验签、validator、一个正确样例和四个错误样例。错误样例覆盖缺回执、缺人审、哈希不匹配、错误保存合同全文等问题。

重点不是证明模型结论正确，而是证明证据规则能发现关键缺口。

## 4. v0.2-alpha 新增了什么

v0.2-alpha 新增 OpenTelemetry（开放遥测标准）风格 trace（追踪记录）到 AEP 的自举验证。这里的 OpenTelemetry 只是风格映射 demo，不是完整兼容实现。

项目提供合成 trace 样例，把工具调用、风险等级、回执、人工审核、来源定位和摘要引用映射到 AEP 证据包，再签名和校验。

## 5. 为什么 validator 比普通日志更重要

日志记录“发生过什么”，validator 检查“证据是否够用”。工具动作如果声明需要 receipt（回执），就必须能找到对应 receipt_id。高风险动作必须有 human_review.approved 为 true。合同审查结论必须指向 source_clause_ref 或 source_location。

## 6. 正确样例和错误样例的意义

只有正确样例不够。证据系统必须能证明错误会失败。RedCrag AEP 的 specimen（样例集）保留错误样例：缺回执会失败，缺人审会失败，证据被改会失败，保存合同全文会失败。

## 7. 怎么运行验证

```bash
python -m redcrag_aep.cli demo
python -m redcrag_aep.cli selfcheck-otel
python -m unittest discover -s tests
```

第一条运行合同审查 demo，第二条运行 OpenTelemetry 风格 trace 自检，第三条运行 unittest（Python 标准库测试框架）回归测试。

## 8. 能证明什么

它能证明证据包结构是否完整、demo 级签名是否匹配、关键动作是否有回执、高风险动作是否有人审、内容哈希是否一致、敏感字段是否被错误写入，以及 OpenTelemetry 风格 trace 能否映射为可校验的 AEP 证据包。

## 9. 不能证明什么

它不能证明模型一定正确，不能替代法律意见，不能保证合规，不能保证安全，也不能证明外部世界事实一定真实。demo 级签名不是生产级法律签名，生产环境需要真实密钥管理和组织流程。

它也没有声称已经接入 Langfuse（开源大语言模型工程平台）或 CozeLoop（扣子罗盘）。

## 10. 下一步路线

下一步不是做 SaaS（Software as a Service，软件即服务）平台，也不是接入真实客户数据。更稳妥的路线是先让公开仓库、Release（发布页）、llms.txt 和 ai-index.json 成为统一引用入口，再做 Langfuse 或 CozeLoop 的文档级适配原型。
