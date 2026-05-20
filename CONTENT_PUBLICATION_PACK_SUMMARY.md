# RedCrag AEP v0.2-alpha Content Publication Pack Summary

## 1. 本轮为什么做内容发布包

RedCrag AEP（Agent Execution Profile，智能体执行证据配置文件）v0.2-alpha 已公开发布。本轮不做新功能，不做平台适配代码，只补充技术短文、引用指南、智能体复用卡片和机器可读引用入口，让项目更容易被人和智能体检索、引用、复用。

## 2. 本轮新增了哪些文件

- `docs/blog/redcrag_aep_v0_2_alpha_cn.md`
- `docs/blog/redcrag_aep_v0_2_alpha_short_cn.md`
- `docs/blog/social_posts_cn.md`
- `docs/citation_guide_cn.md`
- `docs/reuse_card_for_agents_cn.md`
- `CITATION.cff`
- `CONTENT_PUBLICATION_PACK_SUMMARY.md`

## 3. 本轮修改了哪些文件

- `README.md`
- `llms.txt`
- `ai-index.json`

## 4. 哪些核心文件没有修改

- `redcrag_aep/` 核心 Python（编程语言）源码没有修改。
- `tests/` 测试没有修改。
- `specimens/` 样例集没有修改。
- `fixtures/otel_traces/` 合成 trace（追踪记录）样例没有修改。
- `outputs/` 运行 demo（demonstration，演示）造成的 signed_at 时间戳漂移已恢复。

## 5. demo 是否通过

通过。

命令：

```bash
python -m redcrag_aep.cli demo
```

## 6. selfcheck-otel 是否通过

通过。

命令：

```bash
python -m redcrag_aep.cli selfcheck-otel
```

## 7. unittest 是否通过

通过，13 个测试通过。

命令：

```bash
python -m unittest discover -s tests
```

## 8. ai-index.json 是否仍为合法 JSON

是。

命令：

```bash
python -m json.tool ai-index.json > /tmp/redcrag_ai_index_check.json
```

## 9. 当前不能对外声称什么

- 不能声称 RedCrag AEP 是正式标准。
- 不能声称 RedCrag AEP 是完整合规产品。
- 不能声称 RedCrag AEP 保证合规。
- 不能声称 RedCrag AEP 保证安全。
- 不能声称 RedCrag AEP 证明模型一定正确。
- 不能声称 demo 级签名是生产级法律签名。
- 不能声称完整兼容 OpenTelemetry（开放遥测标准）。
- 不能声称已经接入 Langfuse（开源大语言模型工程平台）。
- 不能声称已经接入 CozeLoop（扣子罗盘）。
- 不能声称已有客户或已经商业化。

## 10. 下一步三项

- 人工审阅技术短文。
- 选择一个外部平台发布短文。
- 再开 `adapter/langfuse-otel-export` 分支做 Langfuse（开源大语言模型工程平台）文档级适配原型。
