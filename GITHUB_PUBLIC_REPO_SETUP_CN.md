# GitHub 公开仓库创建说明

## 1. 建议仓库名

`redcrag-aep`

## 2. 建议简介

RedCrag AEP（Agent Execution Profile，智能体执行证据配置文件）给智能体关键动作生成可签名、可校验、可复核的执行证据。

## 3. 建议公开前确认

- `git status` 干净。
- demo（demonstration，演示）通过。
- selfcheck-otel 通过。
- unittest（Python 标准库测试框架）通过。
- `PUBLIC_AUDIT_FINDINGS.md` 已审阅。

## 4. GitHub 网页创建步骤

1. 打开 GitHub（代码托管平台）。
2. 新建 repository（repository，仓库）。
3. 仓库名填写 `redcrag-aep`。
4. 选择 Public（公开）或 Private（私有）。
5. 不勾选初始化 README（README，项目说明文件）。
6. 不添加 `.gitignore`。
7. 不添加 license（license，许可证），除非之后明确选择。

## 5. 本地添加 remote 的命令模板

以下命令只是模板，不要在本次 release freeze 中执行：

```bash
git remote add origin <你的 GitHub 仓库地址>
git push -u origin main
git push origin v0.2-alpha
```

## 6. 许可证建议

暂时不自动添加 LICENSE（license，许可证）文件。

如果要开源，后续再由用户明确选择：

- MIT（Massachusetts Institute of Technology License，麻省理工许可证）
- Apache-2.0（Apache License 2.0，阿帕奇许可证 2.0）
- 其他许可证

没有明确许可证前，公开仓库可以被阅读，但外部复用权利不清晰。正式开放复用前应单独确定许可证。

## 7. 发布文案建议

发布短文可参考：

```text
docs/release_announcement_draft_cn.md
```

发布时应继续保留边界：

- OpenTelemetry（开放遥测标准）只是风格映射 demo（demonstration，演示），不是完整兼容。
- demo（demonstration，演示）级签名不是生产级法律签名。
- 当前没有真实客户数据。
- 当前没有真实平台合作。
- 当前不做 SaaS（Software as a Service，软件即服务）。
