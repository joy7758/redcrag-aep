# RedCrag AEP 公开发布检查清单

公开仓库或发给平台方前，逐项检查：

- [ ] 无真实客户数据。
- [ ] 无合同全文。
- [ ] 无密钥、证书、私钥、API key（Application Programming Interface key，应用程序接口密钥）或云凭据。
- [ ] demo（demonstration，演示）通过。
- [ ] unittest（Python 标准库测试框架）通过。
- [ ] selfcheck-otel 通过。
- [ ] README（项目说明文件）清楚。
- [ ] 边界声明清楚。
- [ ] 没有夸大合规、安全、模型正确性。
- [ ] 没有虚构平台合作。
- [ ] 没有声称完整 OpenTelemetry（开放遥测标准）兼容。
- [ ] 没有声称生产级法律签名。
- [ ] 没有无关大文件或本地缓存文件。

当前 v0.2-alpha 只能表述为 OpenTelemetry（开放遥测标准）风格 trace（追踪记录）映射 demo（demonstration，演示），不能表述为完整平台接入。
