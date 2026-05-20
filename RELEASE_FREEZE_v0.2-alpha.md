# RedCrag AEP v0.2-alpha Public-Ready Release Freeze

## 1. Version Name

RedCrag AEP v0.2-alpha public-ready

## 2. Current Capabilities

- AEP（Agent Execution Profile，智能体执行证据配置文件）最小字段。
- demo（demonstration，演示）级签名。
- validator（validator，校验器）。
- 合同审查 specimen（specimen，样例集）。
- OpenTelemetry（开放遥测标准）风格 trace（追踪记录）到 AEP 映射。
- selfcheck-otel 自检。
- `llms.txt` 智能体检索索引。
- `ai-index.json` 机器可读索引。
- 平台方阅读材料。
- 技术博客草稿。

## 3. Validation Results

Validated locally on 2026-05-20:

- demo（demonstration，演示）通过：`python -m redcrag_aep.cli demo`
- selfcheck-otel 通过：`python -m redcrag_aep.cli selfcheck-otel`
- unittest（Python 标准库测试框架）通过：`python -m unittest discover -s tests`，输出 `Ran 13 tests` 和 `OK`

## 4. Explicit Boundaries

- 不含真实客户数据。
- 不含合同全文。
- 不含密钥。
- 不接真实平台账号。
- 不做 SaaS（Software as a Service，软件即服务）。
- 不完整兼容 OpenTelemetry（开放遥测标准）。
- demo（demonstration，演示）级签名不是生产级法律签名。
- 不保证合规。
- 不保证安全。
- 不证明模型一定正确。

## 5. Next Recommendations

1. 创建远程公开仓库。
2. 发布技术博客。
3. 再选择 Langfuse（开源大语言模型工程平台）或 CozeLoop（扣子罗盘）适配原型。
