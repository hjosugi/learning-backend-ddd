<!-- i18n: language-switcher -->
[English](README.md) | [日本語](README.ja.md)

# Go HTTP API

リクエストルーティング、JSON契約、バリデーション、ユニットテストのための実行可能なGoバックエンドスライス。

## 実行方法

```bash
cd projects/go-http-api
go run .
```

次に以下を実行してください：

```bash
curl http://localhost:8081/healthz
curl http://localhost:8081/tasks
curl -X POST http://localhost:8081/tasks -d '{"title":"learn Go handlers"}'
```

## テスト

```bash
cd projects/go-http-api
go test ./...
```

## 学べること

- `net/http` ハンドラーの境界
- JSONリクエスト/レスポンス契約
- ドメインの変更前のバリデーション
- 振る舞いに関するテーブルテスト