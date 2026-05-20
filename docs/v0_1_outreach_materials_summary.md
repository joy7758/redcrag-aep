# RedCrag AEP v0.1 Outreach Materials Summary

## 1. 本轮新增的对外材料

- `docs/public_demo_walkthrough_cn.md`：面向非技术客户的中文演示讲解稿。
- `docs/trial_package_for_contract_review_cn.md`：合同审查智能体执行证据体检包试点说明。
- `docs/platform_embedding_brief_cn.md`：面向平台商和系统集成商的平台嵌入说明。
- `docs/design_partner_outreach_cn.md`：设计伙伴沟通材料、问题清单、邮件和微信模板。
- `docs/research_note_v0_1_cn.md`：用于论文或标准草案的 v0.1 研究记录。

同时小幅追加了 `README.md` 的 `v0.1 对外材料` 小节。

## 2. 没有被修改的文件

本轮没有修改：

- `redcrag_aep/` 下的 Python（编程语言）源码。
- `specimens/` 样例文件。
- `tests/` 测试文件。
- `schemas/` schema（schema，结构模式）文件。
- `rules/` 规则文件。
- `outputs/` demo（demonstration，演示）证据包文件。

## 3. demo 运行结果

本轮已运行：

```bash
python -m redcrag_aep.cli demo
```

结果：通过，输出包含 `validation_passed: true`。

## 4. tests 运行结果

本轮已运行：

```bash
python -m unittest discover -s tests
```

结果：通过，输出为 `Ran 6 tests` 和 `OK`。

## 5. git commit 状态

本轮文档材料提交为：

```bash
git commit -m "Add RedCrag AEP v0.1 outreach and pilot materials"
```

不执行 `git push`。

## 6. 下一步只建议三件事

1. 人工审阅对外文档措辞。
2. 录制 3 分钟 demo（demonstration，演示）。
3. 找 1 个合同审查或企业客服设计伙伴试点。
