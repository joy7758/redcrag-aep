# RedCrag AEP v0.1 中文演示讲解稿

## 1. 这是什么

RedCrag AEP（Agent Execution Profile，智能体执行证据配置文件）v0.1 是一个最小可运行 demo（demonstration，演示）。它把合同审查智能体的一次关键执行过程，整理成一份可以签名、可以校验、可以复核的证据包。

这里的重点不是再做一个智能体平台，也不是替代合同审查工具本身。RedCrag 关注的是：智能体做了哪些关键动作，这些动作有没有回执，有没有人工审核，证据有没有被改过，记录里有没有不该出现的敏感原文。

## 2. 它解决什么问题

很多智能体系统上线后，真正出问题时很难回答几个基本问题：

- 当时到底调用了什么工具？
- 哪一步属于高风险动作？
- 有没有人工审核？
- 外部系统有没有回执？
- 结论引用了哪一条合同条款？
- 证据记录后来有没有被改？
- 日志里是不是保存了合同全文或敏感信息？

RedCrag AEP v0.1 先用一个小范围合同审查 demo（demonstration，演示）证明：这些问题可以用统一证据包和 validator（validator，校验器）来检查。

## 3. 演示步骤

第一步，运行 demo（demonstration，演示）：

```bash
python -m redcrag_aep.cli demo
```

第二步，展示正确样例：

```text
specimens/contract_review/valid_bundle.json
```

第三步，展示 validator（validator，校验器）通过：

```bash
python -m redcrag_aep.cli validate specimens/contract_review/valid_bundle.json
```

第四步，展示一个错误样例失败，例如缺少人工审核：

```bash
python -m redcrag_aep.cli validate specimens/contract_review/invalid_missing_human_review.json
```

第五步，用普通语言解释通过和失败的原因。

## 4. 正确样例为什么会通过

正确样例会通过，是因为它满足了最小证据要求：

- 有 run id（run identifier，运行标识）。
- 有 workflow（workflow，工作流）和 task（task，任务）说明。
- 有 tool calls（tool calls，工具调用记录）。
- 高风险动作有 human review（human review，人工审核）。
- 需要回执的动作有 receipt（receipt，回执）。
- 合同审查结论有 source clause reference（source clause reference，来源条款引用）。
- 有 content hashes（content hashes，内容哈希）。
- 有 demo（demonstration，演示）级 signature（signature，签名）。

这说明记录结构完整，关键动作能被复查，validator（validator，校验器）可以判断它是否满足规则。

## 5. 错误样例为什么会失败

v0.1 提供四类错误样例，用来证明规则不是摆设：

- `invalid_missing_receipt.json`：工具调用要求 receipt（receipt，回执），但证据包里找不到对应回执。
- `invalid_missing_human_review.json`：高风险动作缺少 approved human review（approved human review，已批准人工审核）。
- `invalid_tampered_hash.json`：输出内容被改过，SHA-256（Secure Hash Algorithm 256-bit，安全哈希算法 256 位）哈希不匹配。
- `invalid_full_contract_leak.json`：证据包里出现 full contract text（full contract text，合同全文）字段，违反隐私最小化边界。

错误样例失败是好事。它说明 validator（validator，校验器）能发现缺回执、缺人审、证据篡改和敏感信息泄露。

## 6. 能证明什么

RedCrag AEP v0.1 能证明：

- 这份证据记录是否具备最小结构。
- demo（demonstration，演示）级签名是否匹配当前内容。
- 关键动作是否有回执。
- 高风险动作是否有人审。
- 合同审查结论是否能指向来源条款。
- 被记录的哈希是否还能对上当前内容。
- 证据包里是否出现了禁止保存的敏感字段名。

## 7. 不能证明什么

RedCrag AEP v0.1 不能证明：

- 模型结论一定正确。
- 外部世界事实一定真实。
- 系统一定已经满足全部法律合规要求。
- 使用方可以自动免责。
- demo（demonstration，演示）级签名等同于生产级法律签名。

当前签名是 HMAC-SHA256-DEMO（Hash-based Message Authentication Code with Secure Hash Algorithm 256-bit demonstration，基于安全哈希算法 256 位的演示级消息认证码），只用于说明证据包可以被签名和验签，不是生产级公私钥签名或法律签名。

## 8. 为什么不保存合同全文

RedCrag 的证据层不应该变成另一个敏感数据仓库。合同全文、客户秘密、私钥、API key（Application Programming Interface key，应用程序接口密钥）等内容不应直接进入 AEP（Agent Execution Profile，智能体执行证据配置文件）证据包。

v0.1 的做法是保存摘要、条款引用、来源位置和 SHA-256（Secure Hash Algorithm 256-bit，安全哈希算法 256 位）哈希。这样既能复核关键动作，又能降低敏感原文扩散风险。

## 9. 下一步如何做试点

下一步不做大平台，也不急着接真实客户数据。建议选择一个边界清楚的合同审查或企业客服智能体，做两周试点：

1. 列出关键动作目录。
2. 标出哪些动作需要 receipt（receipt，回执）。
3. 标出哪些动作需要 human review（human review，人工审核）。
4. 生成 AEP（Agent Execution Profile，智能体执行证据配置文件）证据包。
5. 跑 validator（validator，校验器）。
6. 输出 gap report（gap report，差距报告）。

试点目标不是承诺模型正确，而是证明关键动作能否形成可校验、可复核、可讨论的执行证据。
